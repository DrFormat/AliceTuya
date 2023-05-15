from app.schemas.devices.base_device import BaseDeviceModel


class MCSModel(BaseDeviceModel):
    type: str = 'devices.types.sensor.open'

    class Config:
        title = 'MCS'
