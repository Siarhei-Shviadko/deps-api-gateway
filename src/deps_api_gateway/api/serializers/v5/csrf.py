from pydantic import BaseModel


class CSRFTokenResponseModel(BaseModel):
    token: str
