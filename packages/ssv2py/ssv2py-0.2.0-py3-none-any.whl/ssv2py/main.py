import requests


class SSV2:
    def __init__(
        self, api_url: str = "https://api.funtimes909.xyz", api_key: str = None
    ):
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
        response = requests.get(f"{self.api_url}/stats", headers=self.headers)
        if response.status_code != 200:
            raise ConnectionError(f"Error fetching stats: {response.status_code}")
        return response.json()

    def random(self, minimal: bool = False) -> dict:
        """
        Returns a random server from the SSV2 instance.
        """
        response = requests.get(
            f"{self.api_url}/random", headers=self.headers, params={"minimal": minimal}
        )
        if response.status_code != 200:
            raise ConnectionError(f"Error fetching random: {response.status_code}")
        return response.json()

    def history(
        self, player: str = None, address: str = None, offset: int = 0, limit: int = 10
    ) -> dict:
        """
        Returns a random server from the SSV2 instance.
        """
        if self.api_key is None:
            raise ValueError("API key is required for this method")
        params = {
            "offset": offset,
            "limit": limit,
        }
        if player and not address:
            params["player"] = player
        elif address and not player:
            params["address"] = address
        elif player and address:
            raise ValueError("Cannot use both player and address parameters")
        else:
            raise ValueError("Must use either player or address parameter")
        response = requests.get(
            f"{self.api_url}/random", headers=self.headers, params=params
        )
        if response.status_code != 200:
            raise ConnectionError(f"Error fetching history: {response.status_code}")
        return response.json()
