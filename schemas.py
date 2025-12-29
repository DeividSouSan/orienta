# Schemas used for LLM Output Formats

from pydantic import BaseModel, Field, ConfigDict


class DailyStudySchema(BaseModel):
    """
    Represents the study plan for a given day,
    with goals, research topics, practical activities, and
    learning verification methods.
    """

    model_config = ConfigDict(
        populate_by_name=True
    )  # permite acessar as chaves pelo nome e pelo alias
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
    completed: bool = False
