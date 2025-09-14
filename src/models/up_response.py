from pydantic import BaseModel


class UpResponse(BaseModel):
    status: str
