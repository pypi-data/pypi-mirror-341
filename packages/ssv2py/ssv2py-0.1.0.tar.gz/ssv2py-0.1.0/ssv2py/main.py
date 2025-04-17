import requests


class SSV2:
    def __init__(self, api_url: str, api_key: str = None):
        self.api_url = api_url
        self.api_key = api_key
        if api_url is None:
            raise ValueError("API URL cannot be None")
        if "http://" not in api_url and "https://" not in api_url:
            raise ValueError("API URL must start with http:// or https://")
        self.headers = {"User-Agent": "SSV2Py/0.0.1", "Accept": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"{api_key}"

    def stats(self) -> dict:
        """
        Returns the stats of the SSV2 instance.
        """
        response = requests.get(f"{f'{self.api_url}/stats'}")
        if response.status_code != 200:
            raise Exception(f"Error fetching stats: {response.status_code}")
        return response.json()
