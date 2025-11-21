from dotenv import load_dotenv
import os

import requests
from src.models import guide, user, auth, session

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:5000/api/v1")


def test_update_studies_on_valid_guide(mock_session):
    new_guide = guide.generate_with_metadata(
        title="Test PATCH",
        owner="mock",
        inputs={
            "topic": "Eu quero estudar sobre desenvolvimento backend com foco em Python.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 3,
        },
    )

    new_guide_id = guide.save(new_guide)

    response = mock_session.patch(
        f"{API_URL}/guides/{new_guide_id}",
        headers={"Content-Type": "application/json"},
        json={
            "new_studies_list": [
                {
                    "completed": True,
                    "day": 1,
                    "goal": "Entender o papel de um servidor de aplicação como o Gunicorn no ecossistema Python.",
                    "learning_verification": "Por que uma aplicação web Python não pode se comunicar diretamente com um servidor web como o Nginx sem uma interface como o WSGI?",
                    "practical_activity": "Criar uma aplicação 'Olá, Mundo!' mínima com o framework Flask e executá-la usando o servidor de desenvolvimento embutido.",
                    "theoretical_research": [
                        "O que é um servidor web (ex: Nginx)?",
                        "O que é WSGI (Web Server Gateway Interface)?",
                        "Qual a função de um servidor de aplicação WSGI como o Gunicorn?",
                    ],
                    "title": "Fundamentos: Servidores Web e WSGI",
                },
                {
                    "completed": True,
                    "day": 2,
                    "goal": "Aprender a executar uma aplicação Python com Gunicorn e compreender o conceito fundamental de 'worker'.",
                    "learning_verification": "Se um worker falhar ou travar, o que o processo 'master' do Gunicorn faz para garantir que a aplicação continue funcionando?",
                    "practical_activity": "Pegar a aplicação Flask do dia anterior e executá-la usando o comando 'gunicorn'. Observe os logs de inicialização para identificar os processos sendo criados.",
                    "theoretical_research": [
                        "Como instalar o Gunicorn e iniciar uma aplicação a partir da linha de comando?",
                        "O que é um 'processo worker' no contexto do Gunicorn?",
                        "Qual a diferença entre o processo 'master' e os processos 'worker' do Gunicorn?",
                    ],
                    "title": "Introdução ao Gunicorn e o Conceito de Worker",
                },
                {
                    "completed": False,
                    "day": 3,
                    "goal": "Compreender os diferentes tipos de workers do Gunicorn e como ajustar a quantidade deles para otimizar o desempenho.",
                    "learning_verification": "Em qual tipo de aplicação um worker assíncrono (como gevent) oferece mais vantagens em comparação com o worker síncrono padrão?",
                    "practical_activity": "Execute sua aplicação Gunicorn com diferentes configurações. Primeiro com `-w 4`. Depois, instale o 'gevent' (`pip install gevent`) e execute com `-k gevent -w 4`.",
                    "theoretical_research": [
                        "Tipos de workers do Gunicorn: síncronos (sync) vs. assíncronos (gevent, eventlet).",
                        "Como calcular o número ideal de workers para uma aplicação baseada em CPU (CPU-bound)?",
                        "Parâmetros de linha de comando do Gunicorn: `-w` (workers) e `-k` (worker class).",
                    ],
                    "title": "Configurando Tipos e Quantidade de Workers",
                },
            ]
        },
    )
    assert response.status_code == 200

    response_body: dict[str, str] = response.json()
    assert response_body == {
        "message": "O estado da Studies List foi alterado com sucesso!",
        "data": [
            {
                "day": 1,
                "goal": response_body["data"][0]["goal"],
                "learning_verification": response_body["data"][0][
                    "learning_verification"
                ],
                "practical_activity": response_body["data"][0]["practical_activity"],
                "theoretical_research": response_body["data"][0][
                    "theoretical_research"
                ],
                "title": response_body["data"][0]["title"],
                "completed": True,
            },
            {
                "day": 2,
                "goal": response_body["data"][1]["goal"],
                "learning_verification": response_body["data"][1][
                    "learning_verification"
                ],
                "practical_activity": response_body["data"][1]["practical_activity"],
                "theoretical_research": response_body["data"][1][
                    "theoretical_research"
                ],
                "title": response_body["data"][1]["title"],
                "completed": True,
            },
            {
                "day": 3,
                "goal": response_body["data"][2]["goal"],
                "learning_verification": response_body["data"][2][
                    "learning_verification"
                ],
                "practical_activity": response_body["data"][2]["practical_activity"],
                "theoretical_research": response_body["data"][2][
                    "theoretical_research"
                ],
                "title": response_body["data"][2]["title"],
                "completed": False,
            },
        ],
    }


def test_update_studies_with_unauthorized_user():
    user.create(username="marco", email="marco@orienta.com", password="123456")

    user_data = auth.authenticate("marco@orienta.com", "123456")
    cookie = session.create(user_data["idToken"])

    new_guide = guide.generate_with_metadata(
        title="Tes Unauthorized PATCH",
        owner="mock",
        inputs={
            "topic": "Eu quero estudar sobre desenvolvimento backend com foco em Python.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 3,
        },
    )

    new_guide_id = guide.save(new_guide)

    s = requests.Session()
    s.cookies.set("session_id", cookie)

    response = s.patch(
        f"{API_URL}/guides/{new_guide_id}",
        headers={"Content-Type": "application/json"},
        json={
            "new_studies_list": [
                {
                    "completed": True,
                    "day": 1,
                    "goal": "Entender o papel de um servidor de aplicação como o Gunicorn no ecossistema Python.",
                    "learning_verification": "Por que uma aplicação web Python não pode se comunicar diretamente com um servidor web como o Nginx sem uma interface como o WSGI?",
                    "practical_activity": "Criar uma aplicação 'Olá, Mundo!' mínima com o framework Flask e executá-la usando o servidor de desenvolvimento embutido.",
                    "theoretical_research": [
                        "O que é um servidor web (ex: Nginx)?",
                        "O que é WSGI (Web Server Gateway Interface)?",
                        "Qual a função de um servidor de aplicação WSGI como o Gunicorn?",
                    ],
                    "title": "Fundamentos: Servidores Web e WSGI",
                },
                {
                    "completed": True,
                    "day": 2,
                    "goal": "Aprender a executar uma aplicação Python com Gunicorn e compreender o conceito fundamental de 'worker'.",
                    "learning_verification": "Se um worker falhar ou travar, o que o processo 'master' do Gunicorn faz para garantir que a aplicação continue funcionando?",
                    "practical_activity": "Pegar a aplicação Flask do dia anterior e executá-la usando o comando 'gunicorn'. Observe os logs de inicialização para identificar os processos sendo criados.",
                    "theoretical_research": [
                        "Como instalar o Gunicorn e iniciar uma aplicação a partir da linha de comando?",
                        "O que é um 'processo worker' no contexto do Gunicorn?",
                        "Qual a diferença entre o processo 'master' e os processos 'worker' do Gunicorn?",
                    ],
                    "title": "Introdução ao Gunicorn e o Conceito de Worker",
                },
                {
                    "completed": False,
                    "day": 3,
                    "goal": "Compreender os diferentes tipos de workers do Gunicorn e como ajustar a quantidade deles para otimizar o desempenho.",
                    "learning_verification": "Em qual tipo de aplicação um worker assíncrono (como gevent) oferece mais vantagens em comparação com o worker síncrono padrão?",
                    "practical_activity": "Execute sua aplicação Gunicorn com diferentes configurações. Primeiro com `-w 4`. Depois, instale o 'gevent' (`pip install gevent`) e execute com `-k gevent -w 4`.",
                    "theoretical_research": [
                        "Tipos de workers do Gunicorn: síncronos (sync) vs. assíncronos (gevent, eventlet).",
                        "Como calcular o número ideal de workers para uma aplicação baseada em CPU (CPU-bound)?",
                        "Parâmetros de linha de comando do Gunicorn: `-w` (workers) e `-k` (worker class).",
                    ],
                    "title": "Configurando Tipos e Quantidade de Workers",
                },
            ]
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "name": "UnauthorizedError",
        "message": "Você não tem acesso à esse guia.",
        "action": "Acesse um guia de sua autoria e tente novamente.",
        "code": 401,
    }


def test_update_studies_with_completed_guide(mock_session):
    new_guide = guide.generate_with_metadata(
        title="Completed Guide PATCH",
        owner="mock",
        inputs={
            "topic": "Eu quero estudar sobre desenvolvimento backend com foco em Python.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 3,
        },
    )

    new_guide_id = guide.save(new_guide)

    response = mock_session.patch(
        f"{API_URL}/guides/{new_guide_id}",
        headers={"Content-Type": "application/json"},
        json={
            "new_studies_list": [
                {
                    "completed": True,
                    "day": 1,
                    "goal": "Entender o papel de um servidor de aplicação como o Gunicorn no ecossistema Python.",
                    "learning_verification": "Por que uma aplicação web Python não pode se comunicar diretamente com um servidor web como o Nginx sem uma interface como o WSGI?",
                    "practical_activity": "Criar uma aplicação 'Olá, Mundo!' mínima com o framework Flask e executá-la usando o servidor de desenvolvimento embutido.",
                    "theoretical_research": [
                        "O que é um servidor web (ex: Nginx)?",
                        "O que é WSGI (Web Server Gateway Interface)?",
                        "Qual a função de um servidor de aplicação WSGI como o Gunicorn?",
                    ],
                    "title": "Fundamentos: Servidores Web e WSGI",
                },
                {
                    "completed": True,
                    "day": 2,
                    "goal": "Aprender a executar uma aplicação Python com Gunicorn e compreender o conceito fundamental de 'worker'.",
                    "learning_verification": "Se um worker falhar ou travar, o que o processo 'master' do Gunicorn faz para garantir que a aplicação continue funcionando?",
                    "practical_activity": "Pegar a aplicação Flask do dia anterior e executá-la usando o comando 'gunicorn'. Observe os logs de inicialização para identificar os processos sendo criados.",
                    "theoretical_research": [
                        "Como instalar o Gunicorn e iniciar uma aplicação a partir da linha de comando?",
                        "O que é um 'processo worker' no contexto do Gunicorn?",
                        "Qual a diferença entre o processo 'master' e os processos 'worker' do Gunicorn?",
                    ],
                    "title": "Introdução ao Gunicorn e o Conceito de Worker",
                },
                {
                    "completed": True,
                    "day": 3,
                    "goal": "Compreender os diferentes tipos de workers do Gunicorn e como ajustar a quantidade deles para otimizar o desempenho.",
                    "learning_verification": "Em qual tipo de aplicação um worker assíncrono (como gevent) oferece mais vantagens em comparação com o worker síncrono padrão?",
                    "practical_activity": "Execute sua aplicação Gunicorn com diferentes configurações. Primeiro com `-w 4`. Depois, instale o 'gevent' (`pip install gevent`) e execute com `-k gevent -w 4`.",
                    "theoretical_research": [
                        "Tipos de workers do Gunicorn: síncronos (sync) vs. assíncronos (gevent, eventlet).",
                        "Como calcular o número ideal de workers para uma aplicação baseada em CPU (CPU-bound)?",
                        "Parâmetros de linha de comando do Gunicorn: `-w` (workers) e `-k` (worker class).",
                    ],
                    "title": "Configurando Tipos e Quantidade de Workers",
                },
            ]
        },
    )

    assert response.status_code == 200

    response_body: dict[str, str] = response.json()
    assert response_body == {
        "message": "O estado da Studies List foi alterado com sucesso!",
        "data": [
            {
                "day": 1,
                "goal": response_body["data"][0]["goal"],
                "learning_verification": response_body["data"][0][
                    "learning_verification"
                ],
                "practical_activity": response_body["data"][0]["practical_activity"],
                "theoretical_research": response_body["data"][0][
                    "theoretical_research"
                ],
                "title": response_body["data"][0]["title"],
                "completed": True,
            },
            {
                "day": 2,
                "goal": response_body["data"][1]["goal"],
                "learning_verification": response_body["data"][1][
                    "learning_verification"
                ],
                "practical_activity": response_body["data"][1]["practical_activity"],
                "theoretical_research": response_body["data"][1][
                    "theoretical_research"
                ],
                "title": response_body["data"][1]["title"],
                "completed": True,
            },
            {
                "day": 3,
                "goal": response_body["data"][2]["goal"],
                "learning_verification": response_body["data"][2][
                    "learning_verification"
                ],
                "practical_activity": response_body["data"][2]["practical_activity"],
                "theoretical_research": response_body["data"][2][
                    "theoretical_research"
                ],
                "title": response_body["data"][2]["title"],
                "completed": True,
            },
        ],
    }

    completed_guide = guide.find_guide_by_id(new_guide_id)
    assert completed_guide["status"] == "completed"
    assert completed_guide["completed_at"]
