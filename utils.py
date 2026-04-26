# protected route example
import os
from functools import wraps

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import firestore
from flask import g, request

from errors import UnauthorizedError
from models import session

load_dotenv()


def protected(f):
    """
    Função decoradora para validar autenticação.
    """

    @wraps(f)
    def is_logged(*args, **kwargs):
        session_cookie = request.cookies.get("session_id")

        if not session_cookie:
            raise UnauthorizedError(
                "Cookie de sessão não encontrado.", "Faça login para continuar."
            )

        decoded_claims = session.verify_cookie(session_cookie)
        g.username = decoded_claims.name
        g.email = decoded_claims.email
        g.uid = decoded_claims.uid

        return f(*args, **kwargs)

    return is_logged


def _check(name: str, condition: bool, errors_list: list, error_message: str):
    """
    Função auxiliar para verificar uma condição e reportar o status.
    """
    if condition:
        print(f"  ✔ {name}")
    else:
        print(f"  ❌ {name}")
        errors_list.append(error_message)


def validate_config():
    """
    Verifica todas as variáveis de ambiente e arquivos necessários.
    Levanta um EnvironmentError se qualquer verificação obrigatória falhar.
    """
    errors = []
    ENV = os.getenv("ENVIRONMENT", "development")

    print(f"--- Verificando Variáveis de Ambiente ({ENV}) ---")

    # --- Variáveis Obrigatórias ---
    _check(
        "GOOGLE_APPLICATION_CREDENTIALS",
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None,
        errors,
        "GOOGLE_APPLICATION_CREDENTIALS não está definida.",
    )
    _check(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY") is not None,
        errors,
        "GEMINI_API_KEY não está definida.",
    )
    _check(
        "FIREBASE_API_KEY",
        os.getenv("FIREBASE_API_KEY") is not None,
        errors,
        "FIREBASE_API_KEY não está definida.",
    )

    # --- Variáveis Condicionais ---
    if ENV != "development":
        _check(
            "GOOGLE_SERVICES_JSON",
            os.getenv("GOOGLE_SERVICES_JSON") is not None,
            errors,
            "GOOGLE_SERVICES_JSON é obrigatório em ambientes de produção/staging.",
        )

    print("\n--- Verificando Arquivos ---")

    # --- Verificação de Arquivos ---
    _check(
        "'service-account.json' EXISTE",
        os.path.exists("service-account.json"),
        errors,
        "O arquivo 'service-account.json' não foi encontrado.",
    )

    # --- Relatório Final ---
    if errors:
        print("\n" + "=" * 40)
        print("❌ ERRO DE CONFIGURAÇÃO: O processo vai parar.")
        print("Problemas encontrados:")
        for err in errors:
            print(f"  - {err}")
        print("=" * 40)

        raise EnvironmentError("Configuração inválida.")

    print("\n" + "=" * 40)
    print("🎉 Configuração verificada com sucesso!")
    print("=" * 40)


def initialize_app():
    try:
        firebase_admin.initialize_app()

        db = firestore.client()

        if not db.collection("_internal_status").get():
            db.collection("_internal_status").add({"status": "online"}, "health_check")
            print("🟢 CRIADO: coleção `_internal_status` e documento `health_check`")
        else:
            print(
                "🟡 JÁ EXISTEM: coleção `_internal_status` e documento `health_check`"
            )

        print("🔥 Firebase INICIALIZADO com sucesso!")
    except Exception:
        raise Exception("❌ NÃO FOI POSSÍVEL inicializar o Firebase nesta aplicação!")


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


def load_prompt(file_name: str) -> str:
    """Carrega um arquivo de prompt da pasta /prompts."""

    current = os.getcwd()
    prompt_path = os.path.join(current, "prompts", file_name)

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Erro grave: o prompt não foi encontrado
        raise RuntimeError(
            f"Erro crítico: O arquivo de prompt '{file_name}' não foi encontrado."
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o arquivo de prompt: {e}")
