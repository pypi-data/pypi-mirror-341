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
            self.headers["X-Auth-Key"] = f"{api_key}"

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

    def takedown(self, address: str = None) -> dict:
        """
        Removes a server from the SSV2 Database.
        """
        if self.api_key is None:
            raise ValueError("API key is required for this method")
        if address is None:
            raise ValueError("Address cannot be empty")
        response = requests.post(
            f"{self.api_url}/takedown",
            headers=self.headers,
            params={"address": address},
        )
        if response.status_code != 200:
            raise ConnectionError(f"Error removing server: {response.status_code}")
        return response.json()

    def servers(
        self,
        address: str = None,
        port: int = None,
        version: str = None,
        software: str = None,
        motd: str = None,
        country: str = None,
        asn: str = None,
        org: str = None,
        hostname: str = None,
        icon: bool = None,
        prevents_reports: bool = None,
        whitelist: bool = None,
        cracked: bool = None,
        enforces_secure_chat: bool = False,
        empty: bool = None,
        full: bool = None,
        minimal: bool = None,
        seenafter: int = None,
        seenbefore: int = None,
        onlineplayers: int = None,
        maxplayers: int = None,
        protocol: int = None,
        offset: int = 0,
        limit: int = 10,
    ) -> dict:
        """
        Returns a dict of servers from the SSV2 instance.
        """
        if self.api_key is None and whitelist:
            raise ValueError("API key is required for this query")
        elif self.api_key is None and cracked:
            raise ValueError("API key is required for this query")
        params = {}
        if address:
            params["address"] = address
        if port:
            params["port"] = port
        if version:
            params["version"] = version
        if software:
            params["software"] = software
        if motd:
            params["motd"] = motd
        if country:
            params["country"] = country
        if asn:
            params["asn"] = asn
        if org:
            params["org"] = org
        if hostname:
            params["hostname"] = hostname
        if icon:
            params["icon"] = icon
        if prevents_reports:
            params["prevents_reports"] = prevents_reports
        if whitelist:
            params["whitelist"] = whitelist
        if cracked:
            params["cracked"] = cracked
        if enforces_secure_chat:
            params["enforces_secure_chat"] = enforces_secure_chat
        if empty:
            params["empty"] = empty
        if full:
            params["full"] = full
        if minimal:
            params["minimal"] = minimal
        if seenafter:
            params["seenafter"] = seenafter
        if seenbefore:
            params["seenbefore"] = seenbefore
        if onlineplayers:
            params["onlineplayers"] = onlineplayers
        if maxplayers:
            params["maxplayers"] = maxplayers
        if protocol:
            params["protocol"] = protocol
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        response = requests.get(
            f"{self.api_url}/servers", headers=self.headers, params=params
        )
        if response.status_code != 200:
            raise ConnectionError(
                f"Error fetching servers: {response.status_code}\n{response.text}"
            )
        return response.json()
