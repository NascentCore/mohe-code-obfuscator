from pydantic import BaseModel, ConfigDict


class Error(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    code: str
    message: str
    details: str | None = None
