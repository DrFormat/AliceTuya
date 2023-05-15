from pydantic import BaseModel, Field


class Status(BaseModel):
    status: str = Field(title='Status')
