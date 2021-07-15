"""Thingsboard HTTP API Device module"""

import requests


class TBHTTPClient:
    """Thingsboard HTTP API Device"""

    def __init__(self, host: str, token: str):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.api_base_url = f'{host}/api/v1/{token}/'

    def connect(self):
        """Publish an empty telemetry data to ThingsBoard to test the connection."""
        self.publish_data({}, 'telemetry')

    def publish_data(self, data: dict, endpoint: str):
        """Send data to the ThingsBoard HTTP API."""
        response = self.session.post(f'{self.api_base_url}/{endpoint}', json=data)
        response.raise_for_status()

    def get_data(self, params: dict, endpoint: str) -> dict:
        """Send data to the ThingsBoard HTTP API."""
        response = self.session.get(f'{self.api_base_url}/{endpoint}', params=params)
        response.raise_for_status()
        return response.json()

    def send_telemetry(self, telemetry: dict):
        """Publish telemetry to the ThingsBoard HTTP Device API."""
        self.publish_data(telemetry, 'telemetry')

    def send_attributes(self, attributes: dict):
        """Send attributes to the ThingsBoard HTTP Device API."""
        self.publish_data(attributes, 'attributes')

    def request_attributes(self, client_keys: list = None, shared_keys: list = None) -> dict:
        """Request attributes from the ThingsBoard HTTP Device API."""
        params = {'client_keys': client_keys, 'shared_keys': shared_keys}
        return self.get_data(params=params, endpoint='attributes')

    @classmethod
    def provision(cls, host: str, device_name: str, device_key: str, device_secret: str):
        """Initiate device provisioning through the ThingsBoard HTTP Device API."""
        data = {
            'deviceName': device_name,
            'provisionDeviceKey': device_key,
            'provisionDeviceSecret': device_secret
        }
        response = requests.post(f'{host}/api/v1/provision', json=data)
        response.raise_for_status()
        device = response.json()
        if device['status'] == 'SUCCESS' and device['credentialsType'] == 'ACCESS_TOKEN':
            return cls(host=host, token=device['credentialsValue'])
        return None
