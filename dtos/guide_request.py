import typing
from dataclasses import dataclass

from errors import SchemaError


@dataclass(frozen=True)
class GuideRequest:
    title: str
    topic: str
    knowledge: str
    focus_time: int
    days: int

    @classmethod
    def from_dict(cls, data: dict) -> "GuideRequest":
        missing_fields = []
        wrong_type_fields = []

        type_hints = typing.get_type_hints(cls)

        for field_name, field_type in type_hints.items():
            if field_name not in data.keys():
                missing_fields.append(field_name)
                continue

            if not isinstance(data[field_name], field_type):
                wrong_type_fields.append(field_name)

        if missing_fields:
            raise SchemaError(
                message=f"Os campos {missing_fields} estão faltando.",
                action="Preencha os campos faltantes e tente novamente.",
            )

        if wrong_type_fields:
            raise SchemaError(
                message=f"Erro de tipo nos campos: {wrong_type_fields}.",
                action="Preencha os campos com os dados do tipo certo e tente novamente.",
            )

        return cls(
            title=data["title"],
            topic=data["topic"],
            knowledge=data["knowledge"],
            focus_time=data["focus_time"],
            days=data["days"],
        )
