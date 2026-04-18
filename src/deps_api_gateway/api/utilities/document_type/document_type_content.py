from dataclasses import dataclass
from typing import Any, Optional

__all__ = ["TypeContent"]


@dataclass
class TypeContent:
    id: str
    code: str
    name: str
    engine: Optional[str]
    language: Optional[str]
    fields: list[dict[str, Any]]
    extraction_type: Optional[str]
    in_progress: Optional[bool]
    created_at: Optional[str]
    description: Optional[str]

    @classmethod
    def from_type_service(cls, raw_type_content: dict[str, Any]) -> "TypeContent":
        return cls(
            id=raw_type_content["id"],
            code=raw_type_content["id"],
            name=raw_type_content["documentType"],
            engine=raw_type_content.get("engine"),
            language=raw_type_content.get("language"),
            fields=raw_type_content.get("fields", []),
            extraction_type=raw_type_content.get("extractionType"),
            in_progress=raw_type_content.get("inProgress"),
            created_at=raw_type_content.get("created_at"),
            description=raw_type_content.get("description"),
        )

    @classmethod
    def from_corleone_service(cls, raw_type_content: dict[str, Any]) -> "TypeContent":
        return cls(
            id=raw_type_content["pk"],
            code=raw_type_content["code"],
            name=raw_type_content["name"],
            engine=raw_type_content.get("engine"),
            language=raw_type_content.get("language"),
            fields=raw_type_content.get("fields", []),
            extraction_type=raw_type_content.get("extractionType"),
            in_progress=raw_type_content.get("inProgress"),
            created_at=raw_type_content.get("createdAt"),
            description=raw_type_content.get("description"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "pk": self.id,
            "code": self.code,
            "name": self.name,
            "engine": self.engine,
            "language": self.language,
            "fields": self.fields,
            "extractionType": self.extraction_type,
            "inProgress": self.language,
            "createdAt": self.created_at,
            "description": self.description,
        }
