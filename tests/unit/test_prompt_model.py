import pytest

from src.errors import ValidationError
from src.models import prompt


class TestPromptCreation:
    def test_process_with_empty_dict(self):
        with pytest.raises(ValidationError) as error:
            prompt.process({})

        assert (
            error.value.message
            == "As entradas do usuário não podem ser um dicionário vazio."
        )

    def test_process_with_malformed_data(self):
        data = prompt.process(
            {
                "topic": "   Fotossíntese   ",
                "objective": "   Entender o que acontece antes, durante e depois da fotossíntese e sua importância.   ",
                "study_time": "   60   ",
                "duration_time": "   14   ",
                "knowledge": "   Biologia do ensino médio.   ",
            }
        )

        assert data == {
            "topic": "Fotossíntese",
            "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
            "study_time": "60",
            "duration_time": "14",
            "knowledge": "Biologia do ensino médio.",
        }

    def test_validate_with_invalid_topic(self):
        # topic < 5 caracteres
        with pytest.raises(ValidationError) as error1:
            prompt.build(
                {
                    "topic": 4 * "a",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "60",
                    "duration_time": "14",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error1.value.message
            == "O tópico de estudo precisa ter no mínimo 5 e no máximo 20 caracteres."
        )

        # topic > 20 caracteres
        with pytest.raises(ValidationError) as error2:
            prompt.build(
                {
                    "topic": 51 * "a",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "60",
                    "duration_time": "14",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error2.value.message
            == "O tópico de estudo precisa ter no mínimo 5 e no máximo 20 caracteres."
        )

    def test_validate_with_invalid_objective(self):
        # objective < 10 caracteres
        with pytest.raises(ValidationError) as error1:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": 8 * "a " + "a",  # 9 "palavras"
                    "study_time": "60",
                    "duration_time": "14",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error1.value.message
            == "O objetivo precisa ter no mínimo 10 e no máximo 40 palavras."
        )

        # objective > 40 caracteres
        with pytest.raises(ValidationError) as error2:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": 41 * "a ",  # 41 "palavras"
                    "study_time": "60",
                    "duration_time": "14",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error2.value.message
            == "O objetivo precisa ter no mínimo 10 e no máximo 40 palavras."
        )

    def test_validate_with_invalid_study_time(self):
        # valor não numérico
        with pytest.raises(ValidationError) as error1:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "sessenta",
                    "duration_time": "14",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error1.value.message
            == "O tempo de estudo (minutos) precisa ser um número válido."
        )

        # abaixo do intervalo
        with pytest.raises(ValidationError) as error2:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "10",
                    "duration_time": "14",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error2.value.message
            == "O tempo de estudo precisa estar entre 30 minutos e 8 horas (480 minutos)."
        )

        # acima do intervalo
        with pytest.raises(ValidationError) as error3:
            prompt.build(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "481",
                    "duration_time": "14",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error3.value.message
            == "O tempo de estudo precisa estar entre 30 minutos e 8 horas (480 minutos)."
        )

    def test_validate_with_invalid_duration(self):
        # valor não numérico
        with pytest.raises(ValidationError) as error1:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "60",
                    "duration_time": "quatorze",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error1.value.message
            == "A duração do estudo (dias) precisa ser um número válido."
        )

        # abaixo do intervalo
        with pytest.raises(ValidationError) as error2:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "60",
                    "duration_time": "2",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error2.value.message
            == "A duração do estudo precisa estar entre 3 e 30 dias."
        )

        # acima do intervalo
        with pytest.raises(ValidationError) as error3:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "60",
                    "duration_time": "31",
                    "knowledge": "Biologia do Ensino Médio.",
                }
            )

        assert (
            error3.value.message
            == "A duração do estudo precisa estar entre 3 e 30 dias."
        )

    def test_validate_with_invalid_knowledge(self):
        # knowledge < 10 caracteres
        with pytest.raises(ValidationError) as error1:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                    "study_time": "60",
                    "duration_time": "14",
                    "knowledge": "a",
                }
            )

        assert error1.value.message == "O knowledge deve conter no mínimo 3 palavras."

        # knowledge > 40 caracteres
        with pytest.raises(ValidationError) as error2:
            prompt.validate(
                {
                    "topic": "Fotossíntese",
                    "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",  # 41 "palavras"
                    "study_time": "60",
                    "duration_time": "14",
                    "knowledge": 41 * "a ",
                }
            )

        assert error2.value.message == "O knowledge deve conter no mínimo 3 palavras."

    def test_validate_with_invalid_semantics(self):
        # entrada irrelevante, aleatória
        with pytest.raises(ValidationError):
            prompt.validate(
                {
                    "topic": "Teste",
                    "objective": 10 * "teste ",
                    "study_time": "60",
                    "duration_time": "3",
                    "knowledge": "Testando de novo 1, 2, 3.",
                }
            )

        # entrada com palavrões
        with pytest.raises(ValidationError):
            prompt.validate(
                {
                    "topic": "Bioeletrogenese porra",
                    "objective": "Eu quero ficar bom pra caralho nesse tópico, vambora Gemini!",
                    "study_time": "60",
                    "duration_time": "14",
                    "knowledge": "Sei bosta nenhuma, mas tõ inspirado!",
                }
            )

        # entrada aleatória
        with pytest.raises(ValidationError):
            prompt.validate(
                {
                    "topic": "asgdgsagad",
                    "objective": 10 * "dafsfdsaf ",
                    "study_time": "60",
                    "duration_time": "3",
                    "knowledge": "asdfasdfa de novo 1, 2, 3.",
                }
            )

        # entrada irrelevante
        with pytest.raises(ValidationError):
            prompt.validate(
                {
                    "topic": "Como faço pra ser feliz?",
                    "objective": "Eu preciso de dicas pra ser feliz em 10 dias. Eu estou numa fase muito ruim.",
                    "study_time": "60",
                    "duration_time": "10",
                    "knowledge": "Me ajuda por favor.",
                }
            )

    def test_validate_user_prompt_with_valid_data(self):
        result = prompt.user_prompt(
            {
                "topic": "Fotossíntese",
                "objective": "Entender o que acontece antes, durante e depois da fotossíntese e sua importância.",
                "study_time": "60",
                "duration_time": "14",
                "knowledge": "Biologia do Ensino Médio.",
            }
        )

        assert (
            result
            == """
    <INPUTS>
        <TOPIC>Fotossíntese</TOPIC>
        <OBJECTIVE>Entender o que acontece antes, durante e depois da fotossíntese e sua importância.</OBJECTIVE>
        <DAILY_DEDICATION_IN_MINUTES>60 minutes</DAILY_DEDICATION_IN_MINUTES>
        <DURATION_IN_DAYS>14 days</DURATION_IN_DAYS>
        <KNOWLEDGE>Biologia do Ensino Médio.</KNOWLEDGE>
    </INPUTS>
    """
        )

    def test_user_prompt_with_empty_dict(self):
        with pytest.raises(ValidationError) as error:
            prompt.user_prompt({})

        assert (
            error.value.message
            == "As entradas do usuário não podem ser um dicionário vazio."
        )
