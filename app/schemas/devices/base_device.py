from typing import Optional

from pydantic import BaseModel

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

    class Config:
        title = 'BaseDevice'
