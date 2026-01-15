import pytest


@pytest.mark.vcr
def test_with_valid_input(auth_client):
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
            "owner": response_body["data"]["owner"],
            "inputs": {
                "title": "Generate Valid Guide",
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
