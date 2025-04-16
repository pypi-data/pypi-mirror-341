import requests

class DisposableEmailClient:
    def __init__(self, api_key: str, base_url: str = "https://ded.gossorg.in/v1"):
        self.api_key = api_key
        self.base_url = base_url

    def validate(self, email: str) -> dict:
        response = requests.post(
            f"{self.base_url}/validate",
            json={"email": email, "key": self.api_key},
            timeout=5
        )
        response.raise_for_status()
        return response.json()

