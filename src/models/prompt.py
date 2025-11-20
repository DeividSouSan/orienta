from dotenv import load_dotenv
from src.errors import ServiceError, ValidationError
from google import genai
from pydantic import BaseModel, Field
import google.genai.errors as genai_errors
from src.utils import load_prompt

load_dotenv()


def process(user_input: dict) -> dict:
    """Limpa os dados de entrada removendo espaços.

    Args:
        user_input (dict): Dados de entrada do usuário na forma de dicionário.
    """

    if not user_input:
        raise ValidationError(
            "As entradas do usuário não podem ser um dicionário vazio."
        )

    user_input["topic"] = str(user_input["topic"]).strip()
    user_input["knowledge"] = str(user_input["knowledge"]).strip()
    user_input["focus_time"] = (
        user_input["focus_time"].strip()
        if isinstance(user_input["focus_time"], str)
        else user_input["focus_time"]
    )
    user_input["days"] = (
        user_input["days"].strip()
        if isinstance(user_input["days"], str)
        else user_input["days"]
    )

    return user_input


def validate_topic(topic):
    if not isinstance(topic, str):
        raise ValidationError(
            "O tópico de estudo precisa ser um texto.",
        )

    chars_count = len(topic)
    if not 10 <= chars_count <= 150:
        raise ValidationError(
            "O tópico de estudo precisa ter no mínimo 10 e no máximo 150 caracteres.",
            "Verifique o número de caracteres e tente novamente.",
        )


def validate_relevance(topic):
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

    VALIDATION_MODELS = [
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
    ]

    client = genai.Client()
    system_instruction = load_prompt("topic_validation.md")

    for model_name in VALIDATION_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=topic,
                config={
                    "response_mime_type": "application/json",
                    "system_instruction": system_instruction,
                    "temperature": 0,  # respostas mais consistentes, menos criatividade
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


def validate_focus_time(focus_time) -> None:
    if not isinstance(focus_time, int):
        raise ValidationError("O tempo de foco (minutos) deve ser um número inteiro.")

    # entre 30 minutos e 480 minutos (8 horas)
    if not 30 <= int(focus_time) <= 480:
        raise ValidationError(
            "O tempo de foco precisa estar entre 30 minutos e 8 horas (480 minutos).",
            "Verifique se o campo 'tempo de foco' está preenchido e tente novamente.",
        )


def validate_days(days) -> None:
    if not isinstance(days, int):
        raise ValidationError("O número de dias precisa ser um número inteiro.")

    # entre 3 dias e 30 dias
    if not 3 <= int(days) <= 30:
        raise ValidationError(
            "A duração do estudo precisa estar entre 3 e 30 dias.",
            "Verifique se o campo 'duração' está preenchido e tente novamente.",
        )


def validate_knowledge(knowledge) -> None:
    if not isinstance(knowledge, str):
        raise ValidationError("O conhecimento deve ser um texto.")

    if knowledge not in ["zero", "iniciante", "intermediário"]:
        raise ValidationError(
            "O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
            "Preencha o campo 'knowledge' corretamente e tente novamente.",
        )


def format(user_input: dict) -> str:
    """Transforma os dados de entrada em str para ser utilizado como prompt.

    Args:generate_with_metadata
        user_input (dict): Dados de entrada do usuário na forma de dicionário.
    """

    if not user_input:
        raise ValidationError(
            "As entradas do usuário não podem ser um dicionário vazio."
        )

    return f"""
    <INPUTS>
        <TOPIC>{user_input["topic"]}</TOPIC>
        <KNOWLEDGE>{user_input["knowledge"]}</KNOWLEDGE>
        <FOCUS_TIME>{user_input["focus_time"]} minutes</FOCUSC_TIME>
        <DURATION_IN_DAYS>{user_input["days"]} days</DURATION_IN_DAYS>
    </INPUTS>
    """


def make(user_input: dict) -> str:
    """Realiza a orquestração entre os métodos process(), os métodos de validação e o format().

    Args:
        user_input (dict): Dados de entrada do usuário na forma de dicionário.

    Returns:
        str: Dados de entrada (dict) formatados em prompt (str).
    """
    user_input = process(user_input)

    validate_topic(user_input["topic"])
    validate_knowledge(user_input["knowledge"])
    validate_focus_time(user_input["focus_time"])
    validate_days(user_input["days"])

    return format(user_input)
