import os

import google.genai.errors as genai_errors
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

from dtos.guide_request import GuideRequest
from errors import InternalServerError, ServiceError, ValidationError
from objects.prompt import Prompt
from objects.topic import Topic
from utils import load_prompt

load_dotenv()
try:
    VALIDATION_MODELS = os.environ.get("VALIDATION_MODELS").split("|")
except AttributeError as error:
    raise InternalServerError() from error


def validate_relevance(topic: Topic):
    class ValidationResult(BaseModel):
        class VerifyDetails(BaseModel):
            is_relevant: bool = Field(
                description="Indica se o texto é relevante para um plano de estudos."
            )
            is_bad_language: bool = Field(
                description="Indica se o texto contém linguagem ofensiva."
            )
            is_gibberish: bool = Field(
                description="Indica se o texto é aleatório e sem sentido."
            )

        is_valid: bool = Field(
            description="O veredito final: true se todas as verificações passarem, senão false."
        )

        motive: str = Field(
            description="Uma justificativa clara caso a entrada seja inválida. Se for válida, retorna 'N/A'."
        )

    client = genai.Client()
    system_instruction = load_prompt("topic_validation.md")

    for model_name in VALIDATION_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=topic.value,
                config={
                    "response_mime_type": "application/json",
                    "system_instruction": system_instruction,
                    "temperature": 0,
                    "response_schema": ValidationResult,
                },
            )
            result: ValidationResult = response.parsed  # type: ignore

            if result.is_valid is False:
                raise ValidationError(message=result.motive)

            return result
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


def make(request: GuideRequest) -> str:
    """Realiza a validação semântica e gera o prompt XML.

    Args:
        request (GuideRequest): DTO com os dados de entrada já validados sintaticamente.

    Returns:
        str: Dados de entrada formatados em prompt XML.
    """
    # Validação semântica (IA) — recebe o VO diretamente
    validate_relevance(request.topic)

    # Criação do objeto Prompt e geração do XML
    prompt = Prompt(
        topic=request.topic,
        knowledge=request.knowledge,
        focus_time=request.focus_time,
        days=request.days,
    )

    return prompt.to_xml()
