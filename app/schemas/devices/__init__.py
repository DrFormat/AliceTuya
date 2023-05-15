from app.schemas.devices.mcs import MCSModel
from app.schemas.devices.tdq import TDQModel

device_mapper = {
    'tdq': TDQModel,
    'mcs': MCSModel
}
