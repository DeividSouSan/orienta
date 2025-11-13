from datetime import datetime, timezone
from google import genai
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError
from src.schemas import DailyStudySchema

from src.errors import NotFoundError, ServiceError, UnauthorizedError
from src.models import prompt
from google.api_core import exceptions as api_exceptions
import google.genai.errors as genai_errors

from src.utils import load_prompt


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
                    "completed_days": guide.get("completed_days"),
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
                "title": f"Guia: {guide_doc_ref.id}",
                "completed_days": 0,
                "status": "studying",
                **guide_info,
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
    temperature: int = 2,
) -> list[DailyStudySchema]:
    "Gera um guia de estudos a partir de um prompt."

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

        return response.parsed  # type: ignore
    except (
        api_exceptions.ResourceExhausted,
        api_exceptions.TooManyRequests,
        api_exceptions.PermissionDenied,
        api_exceptions.ServiceUnavailable,  # the model is overloaded
    ):
        raise ServiceError(
            "O modelo não consegiu gerar o conteúdo, a cota foi excedida ou seu acesso o modelo negado."
        )

    except Exception as error:
        raise error


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
    inputs: dict,
    model: str = "",
    is_public: bool = False,
    temperature: int = 2,
) -> dict:
    start_time = datetime.now()

    user_prompt = prompt.make(inputs)

    if model:
        daily_study = generate_with_model(user_prompt, model, temperature)
    else:
        daily_study, model = generate_with_fallback(user_prompt)

    finished_time = datetime.now()

    return {
        "owner": owner,
        "inputs": inputs,
        "model": model,
        "temperature": temperature,
        "generation_time_seconds": int((finished_time - start_time).total_seconds()),
        "daily_study": list(map(lambda study: study.model_dump(), daily_study)),
        "created_at": datetime.now(timezone.utc),
        "is_public": is_public,
    }
