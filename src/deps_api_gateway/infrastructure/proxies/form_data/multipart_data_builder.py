from typing import Any, Optional
from uuid import uuid4

from .form_data import FormData

__all__ = ["FormDataBuilder"]


class FormDataBuilder:
    def __init__(self, fields: Optional[dict[str, str]] = None) -> None:
        self._boundary = uuid4().hex
        self._headers = {"Content-Type": f"multipart/form-data; boundary={self._boundary}"}
        self._fields = fields or {}
        self._files: dict[str, tuple[str, bytes]] = {}
        self._data: list[bytes] = []

    def with_file(self, field_name: str, filename: str, content: bytes) -> "FormDataBuilder":
        self._files[field_name] = (filename, content)

        return self

    def with_field(self, key: str, value: str) -> "FormDataBuilder":
        self._fields[key] = value

        return self

    def with_header(self, key: str, value: Any) -> "FormDataBuilder":
        self._headers[key] = value

        return self

    def build(self) -> FormData:
        self._add_files()
        self._add_fields()
        self._add_end_boundary()

        return FormData(headers=self._headers, data=b"".join(self._data))

    def _add_files(self) -> None:
        for field_name, (filename, content) in self._files.items():
            file_part = (
                (
                    f"--{self._boundary}\r\n"
                    f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
                    "Content-Type: application/octet-stream\r\n\r\n"
                ).encode("utf-8")
                + content
                + "\r\n".encode("utf-8")
            )

            self._data.append(file_part)

    def _add_fields(self) -> None:
        for key, value in self._fields.items():
            # fmt: off
            field_part = (
                f"--{self._boundary}\r\n"
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
                f"{value}\r\n"
            )
            # fmt: on
            self._data.append(field_part.encode("utf-8"))

    def _add_end_boundary(self) -> None:
        self._data.append(f"--{self._boundary}--\r\n".encode("utf-8"))
