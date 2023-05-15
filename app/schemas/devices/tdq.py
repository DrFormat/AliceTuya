from app.schemas.devices.base_device import BaseDeviceModel


class TDQModel(BaseDeviceModel):
    type: str = 'devices.types.switch'

    class Config:
        title = 'MCS'
