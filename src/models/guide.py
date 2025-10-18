from datetime import datetime
from google import genai
from pydantic import BaseModel, Field
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError

from src.errors import ServiceError
from src.models import prompt
from google.genai import errors


class DailyStudySchema(BaseModel):
    """
    Represents the study plan for a given day,
    with goals, research topics, practical activities, and
    learning verification methods.
    """

    day: int = Field(
        ...,
        description="O número do dia no plano de estudos.",
        json_schema_extra={"example": 7},
    )
    title: str = Field(
        ...,
        description="O título ou tema principal do dia.",
        json_schema_extra={"example": "Modelagem: Aplicações e Desafios"},
    )
    goal: str = Field(
        ...,
        alias="Meta do Dia",
        description="O objetivo claro e principal a ser alcançado no dia.",
        json_schema_extra={
            "example": "Aplicar e aprofundar os conhecimentos em Modelagem."
        },
    )
    theoretical_research: list[str] = Field(
        ...,
        alias="O Quê Pesquisar (Teoria)",
        description="Lista de 2 a 3 termos ou perguntas-chave para o aluno pesquisar.",
        json_schema_extra={
            "example": "Pesquise 'Modelagem em diferentes cenários.', 'Desafios comuns na modelagem.'"
        },
    )
    practical_activity: str = Field(
        ...,
        alias="Mão na Massa (Prática)",
        description="Uma tarefa ou atividade prática a serem realizadas para aplicar a teoria.",
        json_schema_extra={"example": "Resolver diferentes exemplos de modelagem."},
    )
    learning_verification: str = Field(
        ...,
        alias="Verificação de Aprendizado",
        description="Questão ou método para o aluno autoavaliar o seu entendimento do conteúdo.",
        json_schema_extra={
            "example": "Como a modelagem pode ser aplicada em diferentes contextos?"
        },
    )


def format_date(date):
    """Transforma um objeto datetime em uma data personalizada como 'DIA de MÊS de ANO'"

    Args:
        date (datetime): o objeto datetime com a data a ser formatada

    Returns:
        str: string com a data formatada
    """
    month = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    return f"{date.day} de {month[date.month]} de {date.year}"


def find_guides(user_id: str) -> list[dict]:
    try:
        db = firestore.client()
        results = db.collection("study_guides").where("user_id", "==", user_id).get()

        guides = list()
        for guide in results:
            guides.append(
                {
                    "id": guide.id,
                    "topic": guide.get("prompt.topic"),
                    "objective": guide.get("prompt.objective"),
                    "duration": guide.get("prompt.duration_time"),
                    "created_at": format_date(guide.get("created_at")),
                }
            )

        return guides
    except FirebaseError as error:
        raise ServiceError(
            "Houve um erro ao buscar os seus guias. Tente novamente mais tarde."
        ) from error


def retrieve_daily_plan(guide_id: str) -> list[dict]:
    try:
        db = firestore.client()
        results = (
            db.collection("study_guides")
            .document(guide_id)
            .collection("daily_plans")
            .get()
        )

        daily_study_list = list()
        for daily_study in results:
            daily_study_list.append(daily_study.to_dict())

        return daily_study_list
    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível recuperar os dados desse guia. Tente novamente mais tarde."
        ) from error


def save(guide_info: dict) -> None:
    try:
        db = firestore.client()
        guide_collection_ref = db.collection("study_guides")

        guide_doc_ref = guide_collection_ref.document()
        guide_doc_ref.set(
            {
                "user_id": guide_info["uid"],
                "prompt": guide_info["inputs"],
                "model": guide_info["model"],
                "temperature": guide_info["temperature"],
                "generation_time_ms": guide_info["generation_time_ms"],
                "created_at": firestore.SERVER_TIMESTAMP,
            }
        )

        daily_plans_subcollection_ref = guide_doc_ref.collection("daily_plans")
        for plan in guide_info["daily_study"]:
            plan_doc_ref = daily_plans_subcollection_ref.document(f"Study_{plan.day}")
            plan_dict = plan.model_dump()
            plan_doc_ref.set(plan_dict)
    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível salvar o guia no banco de dados. Sentimos muito."
        ) from error


def generate(
    user_prompt: str,
    model: str = "gemini-2.0-flash-lite",
    temperature: int = 2,
) -> list[DailyStudySchema]:
    """Gera um guia de estudos a partir de um prompt.

    Args:
        user_prompt: Prompt com as entradas do usuário.

    Return:
        list[DailyStudySchema]: Lista com a saída formatada em DailyStudySchema.
    """
    system_instruction = """
    <ROLE>
        Você é um especialista em design instrucional e um planejador de currículo acadêmico. Sua especialidade é decompor tópicos complexos em roteiros de aprendizagem lógicos e sequenciais para estudantes autônomos. Sua resposta deve ser estruturada, objetiva e seguir rigorosamente as regras definidas."
    </ROLE>

    <TASK>
        Com base nos <INPUTS>, sua tarefa é gerar um Guia de Estudos detalhado, dividido em dias.

        Primeiro, analise o Tempo Total (minutos) = (<DAILY_DEDICATION> * <DURATION_IN_DAYS>) e distribua o conteúdo de forma realista. O plano deve ter uma progressão lógica e coerente: comece o Dia 1 considerando o <KNOWLEDGE> do aluno e aumente a complexidade gradualmente, garantindo que cada dia construa sobre o conhecimento do dia anterior. O <OBJECTIVE> deve receber atenção especial e ser aprofundado na segunda metade do plano.

        **Restrição Crítica:** Seu único trabalho é criar o cronograma. NÃO forneça explicações, aulas ou resumos sobre os tópicos. Apenas liste o que o aluno deve fazer.
    </TAREFA>

    <OUTPUT_FORMAT>
        Formate a saída em JSON. O guia deve ser estruturado exatamente da seguinte forma, sem exceções:

        {{
            "Dia": (Número do Dia),
            "Titulo": (Título Conciso do Dia),
            "Meta do Dia": (Escreva um objetivo claro e alcançável. Ex: "Entender o que é uma variável e como declará-la."),
            "O Quê Pesquisar (Teoria)": (Liste no mínimo 2 a 3 termos ou perguntas-chave para o aluno pesquisar. Ex: "O que são tipos de dados em Python?", "Como atribuir valores a variáveis?"),
            "Mão na Massa (Prática)": (Descreva uma tarefa prática e curta para aplicar a teoria. Ex: "Escrever um código que declare 5 variáveis de tipos diferentes (inteiro, texto, booleano, etc.) e imprima seus valores."),
            "Verificação de Aprendizado": (Crie uma única pergunta conceitual para o aluno se autoavaliar. Ex: "Qual a diferença entre uma variável e um valor constante?")
        }}
    </OUTPUT_FORMAT>

    <EXAMPLE>
        {{
            "Dia": 7,
            "Titulo": "Modelagem: Aplicações e Desafios",
            "Meta do Dia": "Aplicar e aprofundar os conhecimentos em Modelagem.",
            "O Quê Pesquisar (Teoria)": "Modelagem em diferentes cenários.", "Desafios comuns na modelagem.",
            "Mão na Massa (Prática)": "Resolver diferentes exemplos de modelagem.",
            "Verificação de Aprendizado": "Como a modelagem pode ser aplicada em diferentes contextos?"
        }}
    </EXAMPLE>

    INICIE A GERAÇÃO DO GUIA DE ESTUDOS PERSONALIZADO ABAIXO, CERTIFIQUE-SE QUE A SAÍDA É UM JSON VÁLIDO.
    """
    try:
        client = genai.Client()
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

    except errors.APIError as error:
        raise ServiceError(
            "Ocorreu um erro ao tentar gerar o guia. Tente novamente mais tarde."
        ) from error


def build(
    uid: str,
    inputs: dict,
    model: str = "gemini-2.0-flash-lite",
    temperature: int = 2,
) -> dict:
    start_time = datetime.now()
    daily_study = generate(prompt.build(inputs))
    finished_time = datetime.now()

    return {
        "uid": uid,
        "inputs": inputs,
        "model": model,
        "temperature": temperature,
        "generation_time_ms": int((finished_time - start_time).total_seconds()),
        "daily_study": daily_study,
    }
