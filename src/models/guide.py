from datetime import datetime, timezone
from typing import Any
from google import genai
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError
from src.schemas import DailyStudySchema

from src.errors import NotFoundError, ServiceError, UnauthorizedError, ValidationError
from src.models import prompt
import google.genai.errors as genai_errors

from src.utils import load_prompt
from pydantic import TypeAdapter
from pydantic import ValidationError as PydValidationError
from typing import List


def update_studies(guide_id: str, new_studies: list, username: str) -> dict:
    """Atualiza o campo 'daily_study'."""

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
        guide_ref = db.collection("users_guides").document(guide_id)
        guide_snap = guide_ref.get()

        if guide_snap.get("owner") != username:
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


def find_by_username(username: str, only_public: bool = False) -> list[dict]:
    """Busca os guias de um usuário.

    Args:
        username (str): nome do usuário proprietário dos guias
        only_public (bool):
            True: busca APENAS os guias que o usuário marcou como 'is_public: true'.
            False: busca TODOS os guias do usuário em questão.

    Returns:
        list[dict]: uma lista contendo todos os metadados dos guias encontrados.

    Raises:
        ServiceError: se o serviço do Firebase falhar.

    """
    try:
        db = firestore.client()

        guides_snapshots = []
        if only_public:
            guides_snapshots = (
                db.collection("users_guides")
                .where("owner", "==", username)
                .where("is_public", "==", True)
                .get()
            )
        else:
            guides_snapshots = (
                db.collection("users_guides").where("owner", "==", username).get()
            )

        guides_metadata = list()
        for guide in guides_snapshots:
            guides_metadata.append(
                {
                    "id": guide.id,
                    "title": guide.get("title"),
                    "topic": guide.get("inputs.topic"),
                    "days": guide.get("inputs.days"),
                    "daily_studies": guide.get("daily_study"),
                    "created_at": guide.get("created_at"),
                    "status": guide.get("status"),
                }
            )

            if guide.get("status") == "completed":
                guides_metadata[-1].update(
                    {
                        "completed_at": guide.get("completed_at"),
                    }
                )

        return guides_metadata

    except FirebaseError as error:
        raise ServiceError(
            "Ocorreu um erro ao recuperar os guias.", "Tente novamente mais tarde."
        ) from error


def delete(guide_id: str, username: str) -> None:
    """Deleta o guia do banco de dados.

    Args:
        guide_id (str): o ID do guia a ser deletado.
        username (str): o o nodedo usuário que executou a ação de deletar.

    """
    try:
        db = firestore.client()
        guide_ref = db.collection("users_guides").document(guide_id)
        guide_doc = guide_ref.get()

        if guide := guide_doc.to_dict():
            if guide.get("owner") != username:
                raise UnauthorizedError(
                    "Você não tem permissão para deletar esse guia."
                )

            guide_doc.reference.delete()
        else:
            raise NotFoundError(
                "Guia não encontrado.", "Verifique o ID e tente novamente."
            )
    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível deletar o guia.", "Tente novamente mais tarde."
        ) from error


def find_guideline_by_id(guide_id: str) -> list[dict]:
    try:
        db = firestore.client()
        guide_snapshot = db.collection("users_guides").document(guide_id).get()

        daily_study_list = guide_snapshot.get("daily_study")

        return daily_study_list
    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível recuperar os dados desse guia. Tente novamente mais tarde."
        ) from error


def find_guide_by_id(guide_id: str) -> dict[str, Any]:
    try:
        db = firestore.client()
        guide_snapshot = db.collection("users_guides").document(guide_id).get()

        if guide_snapshot.exists:
            return guide_snapshot.to_dict()
        else:
            raise NotFoundError(
                "O guia não foi encontrado.",
                "Verifique que o guia existe e tente novamente.",
            )

    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível recuperar os dados desse guia. Tente novamente mais tarde."
        ) from error


def save(guide_info: dict) -> str:
    """Persiste o guia gerado no banco de dados.

    Args:
        guide_info (dict): guia gerado através de guide.build().

    Returns:
        str: ID do documento salvo no Firestore.
    """
    try:
        db = firestore.client()
        guides_collection_ref = db.collection("users_guides")
        guide_doc_ref = guides_collection_ref.document()
        guide_doc_ref.set(
            {
                **guide_info,
                "status": "studying",
            }
        )

        return guide_doc_ref.id

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
        print("Resposta: ", response)
        return response.parsed
    except Exception as error:
        raise ServiceError(
            "O modelo não consegiu gerar o conteúdo, a cota foi excedida ou seu acesso o modelo negado."
        ) from error


def generate_with_fallback(
    user_prompt: str,
) -> list[DailyStudySchema]:
    """Gera um guia de estudos a partir de um prompt usando fallback de modelos.

    Args:
        user_prompt (str): prompt do usuário com as informações do guia.

    Returns:
        Tuple[DailyStudySchema, str, Literal(2)]: Tupla com a lista com os guias de estudos diários, nome do modelo e temperatura.

    """
    FALLBACK_MODELS_LIST = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"]

    client = genai.Client()

    for model_name in FALLBACK_MODELS_LIST:
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
    owner: str,
    title: str,
    inputs: dict,
    model: str = "",
    is_public: bool = False,
    temperature: float = 2.0,
) -> dict:
    if not title:
        raise ValidationError(
            "O título não pode ser vazio.",
            "Preencha o título do guia e tente novamente.",
        )

    start_time = datetime.now()

    user_prompt = prompt.make(inputs)

    if model:
        daily_study = generate_with_model(user_prompt, model, temperature)
    else:
        daily_study, model = generate_with_fallback(user_prompt)

    finished_time = datetime.now()

    return {
        "owner": owner,
        "title": title,
        "inputs": inputs,
        "model": model,
        "temperature": temperature,
        "generation_time_seconds": int((finished_time - start_time).total_seconds()),
        "daily_study": list(map(lambda study: study.model_dump(), daily_study)),
        "created_at": datetime.now(timezone.utc),
        "is_public": is_public,
    }
