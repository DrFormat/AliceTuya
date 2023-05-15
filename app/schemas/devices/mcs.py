from typing import Any

from app.schemas.devices.base_device import BaseDeviceModel
from app.schemas.devices.capabilities import capabilities_mapper
from app.schemas.devices.properties import properties_mapper


class MCSModel(BaseDeviceModel):
    type: str = 'devices.types.sensor.open'

    def __init__(self, **data: Any):
        super().__init__(**data)
        if 'status' in data:
            for status in data['status']:
                if status['code'] in capabilities_mapper:
                    self.capabilities.append(capabilities_mapper[status['code']](**status))
                if status['code'] in properties_mapper:
                    self.properties.append(properties_mapper[status['code']](**status))

    class Config:
        title = 'MCS'
