from typing import Any

from pydantic import BaseModel


class SwitchModel(BaseModel):
    type: str = 'devices.capabilities.on_off'
    state: dict = {'instance': 'on', 'value': False}

    def __init__(self, **data: Any):
        super().__init__(**data)
        if 'value' in data:
            self.state['value'] = data['value']

    class Config:
        title = 'Switch'
