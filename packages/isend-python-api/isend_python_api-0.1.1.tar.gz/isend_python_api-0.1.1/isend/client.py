import requests
import json

class Client:
    def __init__(self, auth_token):
        if not auth_token:
            raise ValueError("auth_token is required")
        self.auth_token = auth_token

    def send_email(self, template_name, to_address, data_mapping):
        endpoint = "https://www.trumarry.com/v1/sendEmail"
        return self._send(endpoint, {
            "auth_token": self.auth_token,
            "template_name": template_name,
            "email": to_address,
            "data_mapping": data_mapping
        })

    def send_event(self, event_name, customer_email, properties):
        endpoint = "https://www.trumarry.com/v1/sendEvent"
        return self._send(endpoint, {
            "auth_token": self.auth_token,
            "name": event_name,
            "email": customer_email,
            "properties": properties
        })

    def _send(self, endpoint, payload):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
            return response.json()
        except Exception as e:
            return {"success": False, "message": str(e)}
