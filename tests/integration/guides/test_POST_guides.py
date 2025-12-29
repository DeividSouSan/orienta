import pytest


@pytest.mark.vcr
def test_generate_guide_with_valid_input(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Generate Valid Guide",
            "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 3,
        },
    )

    assert response.status_code == 201

    response_body = response.get_json()

    assert response_body == {
        "message": "Guia de estudos gerado com sucesso.",
        "data": {
            "title": "Generate Valid Guide",
            "owner": response_body["data"]["owner"],
            "inputs": {
                "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
                "knowledge": "zero",
                "focus_time": 60,
                "days": 3,
            },
            "model": response_body["data"]["model"],
            "temperature": 2.0,
            "generation_time_seconds": response_body["data"]["generation_time_seconds"],
            "daily_study": response_body["data"][
                "daily_study"
            ],  # ! Validar pelo número de dias
            "created_at": response_body["data"][
                "created_at"
            ],  # ! Validar se ocorreu no passado
            "is_public": False,
        },
    }


@pytest.mark.vcr
def test_generate_guide_with_specific_model(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Use Specific Model",
            "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
            "knowledge": "iniciante",
            "focus_time": 60,
            "days": 3,
            "model": "gemini-2.5-flash-lite",
            "temperature": 1.0,
        },
    )

    assert response.status_code == 201

    response_body = response.get_json()

    assert response_body == {
        "message": "Guia de estudos gerado com sucesso.",
        "data": {
            "owner": response_body["data"]["owner"],
            "title": "Use Specific Model",
            "inputs": {
                "topic": "Eu quero entender o que são os workers que eu tenho que configurar, por exemplo, no gunicorn.",
                "knowledge": "iniciante",
                "focus_time": 60,
                "days": 3,
            },
            "model": "gemini-2.5-flash-lite",
            "temperature": 1.0,
            "generation_time_seconds": response_body["data"]["generation_time_seconds"],
            "daily_study": response_body["data"]["daily_study"],
            "created_at": response_body["data"]["created_at"],
            "is_public": False,
        },
    }


def test_generate_guide_with_str_focus_time_and_days(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Wrong Types",
            "topic": "Eu quero estudar sobre neurociência.",
            "knowledge": "iniciante",
            "focus_time": "60",
            "days": "3",
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O tempo de foco (minutos) deve ser um número inteiro.",
        "action": response_body["action"],
        "code": 400,
    }


def test_generate_guide_without_topic(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Missing Topic",
            "knowledge": "iniciante",
            "focus_time": 60,
            "days": 3,
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O tópico de estudo precisa ter no mínimo 10 e no máximo 150 caracteres.",
        "action": "Verifique o número de caracteres e tente novamente.",
        "code": 400,
    }


def test_generate_guide_without_knowledge(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Missing Knowledge",
            "topic": "Eu quero estudar sobre a segunda guerra mundial.",
            "focus_time": 60,
            "days": 3,
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O conhecimento deve ser 'zero', 'iniciante' ou 'intermediário'.",
        "action": "Preencha o campo 'knowledge' corretamente e tente novamente.",
        "code": 400,
    }


def test_generate_guide_without_focus_time(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Missing Focus Time",
            "topic": "Eu quero estudar sobre Git e quais seus principais comandos.",
            "knowledge": "zero",
            "days": 3,
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O tempo de foco (minutos) deve ser um número inteiro.",
        "action": response_body["action"],
        "code": 400,
    }


def test_generate_guide_without_days(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "title": "Missing Days",
            "topic": "Quero estudar sobre a revolução russa e como e por que ela aconteceu.",
            "knowledge": "zero",
            "focus_time": 60,
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O número de dias precisa ser um número inteiro.",
        "action": response_body["action"],
        "code": 400,
    }


def test_generate_guide_title(auth_client):
    response = auth_client.post(
        "/api/v1/guides",
        json={
            "topic": "Quero estudar sobre a revolução russa e como e por que ela aconteceu.",
            "knowledge": "zero",
            "focus_time": 60,
            "days": 3,
        },
    )

    assert response.status_code == 400

    response_body = response.get_json()

    assert response_body == {
        "name": "ValidationError",
        "message": "O título não pode ser vazio.",
        "action": "Preencha o título do guia e tente novamente.",
        "code": 400,
    }


def test_anonymous_user(client):
    response = client.post(
        "/api/v1/guides",
        json={
            "title": "Missing Days",
            "topic": "Quero estudar sobre a revolução russa e como e por que ela aconteceu.",
            "knowledge": "zero",
            "focus_time": 60,
        },
    )

    assert response.status_code == 401
