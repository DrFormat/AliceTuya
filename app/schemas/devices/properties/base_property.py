from typing import Any

from pydantic import BaseModel


class BasePropertyModel(BaseModel):
    type: str
    retrievable: bool = True
    reportable: bool = True
    parameters: dict
    state: dict

    def __init__(self, **data: Any):
        super().__init__(**data)
        if 'value' in data:
            self.state['value'] = data['value']

    class Config:
        title = 'BaseProperty'
