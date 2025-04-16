import requests


class Socketnest:
    def __init__(self, app_id: str, secret: str, *args, **kwargs):
        self.app_id = app_id
        self.secret = secret
        self.api_url = "https://api.socketnest.com"

    def trigger(
        self, channel: str, event: str, data: dict,
    ):
        """
        Trigger an event on a SocketNest channel.
        Args:
            channel (str): The channel name.
            event (str): The event name.
            data (dict): The event data.
        Returns:
            requests.Response: The response object from the API call.
        """
        headers = {
            "x-app-id": str(self.app_id),
            "x-secret": str(self.secret),
            "Content-Type": "application/json"
        }
        payload = {
            "channel": channel,
            "event": event,
            "data": data
        }
        endpoint = f"{self.api_url}/trigger"
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response
