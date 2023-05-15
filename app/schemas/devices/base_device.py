from typing import Optional, Any

from pydantic import BaseModel

from app.schemas.devices.capabilities import capabilities_mapper
from app.schemas.devices.properties import properties_mapper
from app.schemas.devices.properties.base_property import BasePropertyModel


class DeviceInfoModel(BaseModel):
    manufacturer: str
    model: str
    hw_version: str
    sw_version: str

    class Config:
        title = 'DeviceInfo'


class BaseDeviceModel(BaseModel):
    id: str
    name: str
    type: str
    capabilities: list = []
    properties: list[BasePropertyModel] = []
    device_info: Optional[DeviceInfoModel]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if 'status' in data:
            for status in data['status']:
                if status['code'] in capabilities_mapper:
                    self.capabilities.append(capabilities_mapper[status['code']](**status))
                if status['code'] in properties_mapper:
                    self.properties.append(properties_mapper[status['code']](**status))

    class Config:
        title = 'BaseDevice'
