from typing import Any

from app.schemas.devices.properties.base_property import BasePropertyModel


class DoorContactStateModel(BasePropertyModel):
    type: str = 'devices.properties.event'
    parameters: dict = {
        'instance': 'open',
        'events': [
            {'name': 'открыто', 'value': 'opened'},
            {'name': 'закрыто', 'value': 'closed'}
        ]
    }
    state: dict = {'instance': 'open', 'value': None}

    def __init__(self, **data: Any):
        super().__init__(**data)
        if 'value' in data:
            self.state['value'] = 'opened' if data['value'] else 'closed'

    class Config:
        title = 'DoorContactState'
