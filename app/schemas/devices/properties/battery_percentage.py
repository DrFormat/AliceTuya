from app.schemas.devices.properties.base_property import BasePropertyModel


class BatteryPercentageModel(BasePropertyModel):
    type: str = 'devices.properties.float'
    parameters: dict = {'instance': 'battery_level', 'unit': 'unit.percent'}
    state: dict = {'instance': 'battery_level', 'value': 10}

    class Config:
        title = 'BatteryPercentage'
