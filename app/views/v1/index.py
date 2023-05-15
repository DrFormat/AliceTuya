from typing import Optional

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from app.schemas.devices import device_mapper
from app.schemas.devices.base_device import BaseDeviceModel
from app.schemas.responses import ResponseModel

router = APIRouter(redirect_slashes=True, prefix='/v1.0', tags=['v1.0'])


def parse_device(tuya_device: dict) -> Optional[dict]:
    product_category = tuya_device.get('category')
    if product_category in device_mapper:
        device_map = device_mapper.get(product_category, None)
        if device_map:
            parsed_device: BaseDeviceModel = device_map(**tuya_device)
            return parsed_device.dict()
    return None


@router.head('/')
def service_available():
    return Response()


@router.post('/user/unlink')
async def user_unlink(request: Request):
    return Response()


@router.get('/user/devices', response_model=ResponseModel)
def devices(request: Request):
    print(f'[headers] {request.headers}')
    tuya_devices = request.app.tcc.get_user_devices()
    alice_devices = []
    for tuya_device in tuya_devices:
        parsed_device = parse_device(tuya_device)
        if parsed_device:
            alice_devices.append(parsed_device)
    response = {
        'request_id': request.headers.get('x-request-id'),
        'payload': {
            'user_id': 'format',
            'devices': alice_devices
        }
    }
    return ResponseModel.parse_obj(response)


@router.post('/user/devices/query', response_model=ResponseModel)
async def devices_query(request: Request):
    try:
        data = await request.json()
        alice_devices = []
        for device in data.get('devices'):
            tuya_device = request.app.tcc.get_device_details(device.get('id'))
            parsed_device = parse_device(tuya_device)
            if parsed_device:
                alice_devices.append(parsed_device)
        response = {
            "request_id": request.headers.get('x-request-id'),
            'payload': {
                'user_id': 'format',
                'devices': alice_devices
            }
        }
        return ResponseModel.parse_obj(response)
    except Exception:
        return Response(status_code=200)


@router.post('/user/devices/action')
async def devices_action(request: Request):
    try:
        data = await request.json()
        devices_response = []
        for device in data.get('payload').get('devices'):
            capabilities_response = []
            for capability in device.get('capabilities'):
                commands = [{
                    "code": "switch_1",
                    "value": capability.get('state').get('value')
                }]
                exec_result = request.app.tcc.exec_device_command(device.get('id'), {"commands": commands})
                capabilities_response.append(
                    {
                        "type": "devices.capabilities.on_off",
                        "state": {
                            "instance": "on",
                            "action_result": {
                                "status": "DONE"
                            }
                        }
                    }
                )

            devices_response.append(
                {
                    "id": device.get('id'),
                    "capabilities": capabilities_response
                }
            )
        response = {
            "request_id": request.headers.get('x-request-id'),
            "payload": {
                "devices": devices_response
            }
        }
        return response
    except Exception:
        return Response()
