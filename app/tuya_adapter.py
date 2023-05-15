import time

import requests
from tuya_iot import TuyaOpenAPI, AuthType, TuyaOpenMQ

from app.core.config import config


class TuyaAdapder(TuyaOpenAPI):
    def __init__(self, endpoint: str, access_id: str, access_secret: str, username: str, password: str):
        super().__init__(endpoint, access_id, access_secret, auth_type=AuthType.SMART_HOME)
        self.connect(username, password, '7', 'SmartLife')
        self._uid = self.token_info.uid

        self.token_info.expire_time = 0

        # self.openmq = TuyaOpenMQ(self)
        # self.openmq.start()
        # self.openmq.add_message_listener(self.on_message)

    # def __del__(self):
    #     self.openmq.remove_message_listener(self.on_message)
    #     self.openmq.stop()

    def on_message(self, msg):
        print('on_message: %s' % msg)
        data = msg.get('data')
        if 'status' in data:
            requests.post(f'https://dialogs.yandex.net/api/v1/skills/{config.SKILL_ID}/callback/state',
                          headers={'Authorization': f'OAuth {config.SKILL_TOKEN}'},
                          json={
                              'ts': time.time(),
                              'payload': {
                                  'user_id': 'format',
                                  'devices': [
                                      {
                                          'id': data.get('devId'),
                                          'properties': [
                                              {
                                                  'type': 'devices.properties.event',
                                                  'state': {
                                                      'instance': 'open',
                                                      'value': 'opened' if data['status'][0]['value'] else 'closed'
                                                  }
                                              }
                                          ]
                                      }
                                  ]
                              }
                          })

    def get_user_devices(self):
        response = self.get(f'/v1.0/users/{self._uid}/devices')
        if not response or not response['success']:
            raise Exception('Fail query devices')
        return response['result']

    def get_device_details(self, device_id=None):
        if not device_id:
            raise Exception("Missing Function Parameters")
        response = self.get(f'/v1.0/devices/{device_id}')
        if not response or not response['success']:
            raise Exception('Fail query device details')
        return response['result']

    def exec_device_command(self, device_id=None, commands=None):
        if not device_id or not commands:
            raise Exception("Missing Function Parameters")
        return self.post(f'/v1.0/devices/{device_id}/commands', commands)
