import os
from datetime import datetime, timezone
from typing import List, Tuple

import dotenv
import google.genai.errors as genai_errors
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError
from google import genai
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import TypeAdapter
from pydantic import ValidationError as PydValidationError

from dtos.guide import GuideDTO
from dtos.guide_request import GuideRequest
from errors import (
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    ServiceError,
    UnauthorizedError,
    ValidationError,
)
from objects.guide_id import GuideId
from objects.prompt import Prompt
from objects.username import Username
from schemas import DailyStudySchema
from utils import load_prompt

dotenv.load_dotenv()

try:
    GEN_MODELS = os.environ.get("GEN_MODELS").split("|")
except AttributeError as error:
    raise InternalServerError() from error


def update_studies(guide_id: GuideId, new_studies: list, username: Username) -> dict:
    """Atualiza o campo 'daily_study'."""

    # Validação básica de entrada
    if not isinstance(new_studies, list):
        raise ValidationError(
            "O campo 'new_studies_state' enviado não é uma lista.",
            "Certifique-se de que o campor é uma lista e tente novamente.",
        )

    try:
        studies_list_adapter = TypeAdapter(List[DailyStudySchema])
        studies_list_adapter.validate_python(new_studies)

        guide_is_complete = all(study["completed"] for study in new_studies)

        db = firestore.client()
        guide_ref = db.collection("users_guides").document(guide_id.value)
        guide_snap = guide_ref.get()

        if guide_snap.get("owner") != username.value:
            raise UnauthorizedError(
                "Você não tem acesso à esse guia.",
                "Acesse um guia de sua autoria e tente novamente.",
            )

        if guide_is_complete:
            guide_ref.update(
                {"status": "completed", "completed_at": datetime.now(timezone.utc)}
            )
        else:
            guide_ref.update({"status": "studying"})

        guide_ref.update({"daily_study": new_studies})

        new_guide_snap = guide_ref.get()
        db_new_studies: list = new_guide_snap.get("daily_study")

        return db_new_studies

    except PydValidationError as error:
        raise ValidationError(
            "O campo 'new_studies_state' é inválido.",
            "Verifique se o corpo da requisição é uma List[DailyStudySchema] e tente novamente.",
        ) from error

    except FirebaseError as error:
        raise ServiceError(
            "Ocorreu um erro ao recuperar os guias.", "Tente novamente mais tarde."
        ) from error


def find_all_by_username(
    username: Username, only_public: bool = False
) -> list[GuideDTO]:
    """Busca os guias de um usuário, ignora os guias que foram deletados."""
    try:
        db = firestore.client()

        guides_snapshots = list()
        if only_public:
            guides_snapshots = (
                db.collection("users_guides")
                .where(filter=FieldFilter("owner", "==", username.value))
                .where(filter=FieldFilter("is_public", "==", True))
                .where(filter=FieldFilter("status", "!=", "deleted"))
                .get()
            )
        else:
            guides_snapshots = (
                db.collection("users_guides")
                .where(filter=FieldFilter("owner", "==", username.value))
                .where(filter=FieldFilter("status", "!=", "deleted"))
                .get()
            )

        guides = list()
        for snap in guides_snapshots:
            data = snap.to_dict()
            data["id"] = snap.id
            guides.append(GuideDTO.from_dict(data))

        return guides

    except FirebaseError as error:
        raise ServiceError(
            "Ocorreu um erro ao recuperar os guias.", "Tente novamente mais tarde."
        ) from error


def delete(guide_id: GuideId, username: Username) -> None:
    """Realiza o SOFT DELETE do guia no banco de dados."""
    try:
        db = firestore.client()
        guide_ref = db.collection("users_guides").document(guide_id.value)
        guide_snap = guide_ref.get()

        if guide := guide_snap.to_dict():
            if guide.get("owner") != username.value:
                raise ForbiddenError(
                    "Você não tem permissão para deletar esse guia.",
                    "Verifique se o guia é de sua autoria e tente novamente.",
                )

            guide_ref.update({"status": "deleted"})
        else:
            raise NotFoundError(
                "Guia não encontrado.", "Verifique o ID e tente novamente."
            )
    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível deletar o guia.", "Tente novamente mais tarde."
        ) from error


def find_by_id(guide_id: GuideId) -> GuideDTO:
    """Busca um Guia pelo seu ID."""
    try:
        db = firestore.client()
        guide_snapshot = db.collection("users_guides").document(guide_id.value).get()

        if guide_snapshot.exists and guide_snapshot.get("status") != "deleted":
            data = guide_snapshot.to_dict()
            data["id"] = guide_snapshot.id
            return GuideDTO.from_dict(data)
        else:
            raise NotFoundError(
                "O guia não foi encontrado.",
                "Verifique que o guia existe e tente novamente.",
            )

    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível recuperar os dados desse guia. Tente novamente mais tarde."
        ) from error


def save(guide: GuideDTO) -> GuideDTO:
    """Persiste o guia gerado no banco de dados."""
    try:
        db = firestore.client()
        guides_collection_ref = db.collection("users_guides")
        guide_doc_ref = guides_collection_ref.document()

        guide_data = guide.to_dict()
        guide_data["status"] = "studying"

        guide_doc_ref.set(guide_data)

        data = guide_doc_ref.get().to_dict()
        data["id"] = guide_doc_ref.id
        return GuideDTO.from_dict(data)

    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível salvar o guia no banco de dados. Sentimos muito."
        ) from error


def generate_with_model(
    user_prompt: str,
    model: str = "gemini-2.0-flash-lite",
    temperature: float = 2.0,
) -> list[DailyStudySchema]:
    """Gera um guia de estudos a partir de um prompt."""

    client = genai.Client()

    try:
        system_instruction = load_prompt("generate_guide.md")
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config={
                "system_instruction": system_instruction,
                "response_mime_type": "application/json",
                "response_schema": list[DailyStudySchema],
                "temperature": temperature,
            },
        )

        return response.parsed
    except Exception as error:
        raise ServiceError(
            "O modelo não consegiu gerar o conteúdo, a cota foi excedida ou seu acesso o modelo negado."
        ) from error


def generate_with_fallback(
    user_prompt: str,
) -> Tuple[List[DailyStudySchema], str]:
    """Gera um guia de estudos a partir de um prompt usando fallback de modelos."""

    client = genai.Client()

    for model_name in GEN_MODELS:
        try:
            system_instruction = load_prompt("generate_guide.md")
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config={
                    "system_instruction": system_instruction,
                    "response_mime_type": "application/json",
                    "response_schema": list[DailyStudySchema],
                    "temperature": 2,
                },
            )

            return response.parsed, model_name  # type: ignore

        except genai_errors.ServerError as error:
            if error.code == 503:
                continue

        except genai_errors.ClientError as error:
            if error.code == 429:
                continue

        except Exception as error:
            raise error

    raise ServiceError(
        "O modelo não consegiu gerar o conteúdo, a cota foi excedida ou seu acesso o modelo negado."
    )


def generate_with_metadata(
    owner: Username,
    inputs: GuideRequest,
    is_public: bool = False,
) -> GuideDTO:
    """Gera um guia de estudos e seus metadados."""

    start_time = datetime.now()

    # Criação do Prompt VO para geração do XML
    prompt_vo = Prompt(
        topic=inputs.topic,
        knowledge=inputs.knowledge,
        focus_time=inputs.focus_time,
        days=inputs.days,
    )

    daily_study, model = generate_with_fallback(prompt_vo.to_xml())

    finished_time = datetime.now()

    return GuideDTO(
        owner=owner,
        inputs=inputs,
        model=model,
        temperature=2.0,
        generation_time_seconds=int((finished_time - start_time).total_seconds()),
        daily_study=list(map(lambda study: study.model_dump(), daily_study)),
        created_at=datetime.now(timezone.utc),
        is_public=is_public,
    )
