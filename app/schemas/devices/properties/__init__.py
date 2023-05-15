from .battery_percentage import BatteryPercentageModel
from .doorcontact_state import DoorContactStateModel

properties_mapper = {
    'doorcontact_state': DoorContactStateModel,
    'battery_percentage': BatteryPercentageModel
}
