import time
from typing import Optional

from pydantic import BaseModel

from app.schemas.devices.base_device import BaseDeviceModel


class PayloadModel(BaseModel):
    user_id: str
    devices: list[BaseDeviceModel]

    class Config:
        title = 'Payload'


class ResponseModel(BaseModel):
    request_id: Optional[str] = ''
    ts: float = time.time()
    payload: PayloadModel

    class Config:
        title = 'Response'
