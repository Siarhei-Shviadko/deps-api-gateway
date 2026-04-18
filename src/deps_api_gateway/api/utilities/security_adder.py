from typing import Any

__all__ = ["add_security_to_openapi"]


def add_security_to_openapi(openapi_schema: dict[str, Any]) -> None:
    security_schema = {
        "securitySchemes": {
            "Bearer Auth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        },
    }

    openapi_schema["security"] = [{"Bearer Auth": []}]

    if openapi_schema.get("components"):
        openapi_schema["components"].update(security_schema)
    else:
        openapi_schema["components"] = security_schema
