from datetime import datetime, timezone
from google import genai
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError
from src.schemas import DailyStudySchema

from src.errors import NotFoundError, ServiceError, UnauthorizedError
from src.models import prompt
from google.api_core import exceptions as api_exceptions
import google.genai.errors as genai_errors


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
                    "topic": guide.get("inputs.topic"),
                    "objective": guide.get("inputs.objective"),
                    "duration": guide.get("inputs.duration_time"),
                    "created_at": guide.get("created_at"),
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
        guide_doc_ref.set(guide_info)

        return guide_doc_ref.id

    except FirebaseError as error:
        raise ServiceError(
            "Não foi possível salvar o guia no banco de dados. Sentimos muito."
        ) from error


def generate(
    user_prompt: str,
    model: str = "gemini-2.0-flash-lite",
    temperature: int = 2,
) -> list[DailyStudySchema]:
    "Gera um guia de estudos a partir de um prompt."

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
    temperature: int = 2,
) -> list[DailyStudySchema]:
    """Gera um guia de estudos a partir de um prompt usando fallback de modelos.

    Args:
        user_prompt (str): prompt do usuário com as informações do guia.
        tempreature (int): nível de criatividade do modelo (0 - 2)

    Returns:
        list[DailyStudySchema]: lista com os guias de estudos diários.

    """
    print("⚠⚠⚠ O MODELO ESTÁ EM MODO DE FALLBACK!!!")
    FALLBACK_MODELS_LIST = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash"]

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

    client = genai.Client()

    for model_name in FALLBACK_MODELS_LIST:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config={
                    "system_instruction": system_instruction,
                    "response_mime_type": "application/json",
                    "response_schema": list[DailyStudySchema],
                    "temperature": temperature,
                },
            )

            return response.parsed  # type: ignore

        except genai_errors.ServerError as error:
            if error.code == 503:
                continue

        except genai_errors.ClientError as error:
            if error.code == 429:
                continue

        except Exception as error:
            print("⚠⚠⚠ O ERRO NÃO FOI CAPTURADO DIREITO!!!")
            raise error

    raise ServiceError(
        "O modelo não consegiu gerar o conteúdo, a cota foi excedida ou seu acesso o modelo negado."
    )


def generate_with_metadata(
    owner: str,
    inputs: dict,
    model: str | None = None,
    is_public: bool = False,
    temperature: int = 2,
    validation_type: str = "both",
) -> dict:
    start_time = datetime.now()

    user_prompt = prompt.build(inputs, validation_type)

    if model:
        daily_study = generate(user_prompt, model, temperature)
    else:
        daily_study = generate_with_fallback(user_prompt, temperature)

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
