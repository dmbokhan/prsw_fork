import datetime
import requests

from typing import Optional

API_URL = "https://stat.ripe.net/data"


class RequestError(Exception):
    """Error class for wrapping request errors."""

    pass


class ResponseError(Exception):
    """Error class for wrapping API response errors."""

    pass


class Output:
    """Object used to hold the response and metadata from the API."""

    def __init__(
        self,
        _url,
        messages: Optional[list] = [],
        see_also: Optional[list] = [],
        version: Optional[str] = "",
        data_call_status: Optional[str] = "",
        cached: Optional[bool] = None,
        data=None,
        query_id: Optional[str] = "",
        process_time: Optional[int] = 0,
        server_id: Optional[str] = "",
        build_version: Optional[str] = "",
        status: Optional[str] = "",
        status_code: Optional[int] = 0,
        time: Optional[str] = "",
    ):
        """Initialize the Output object."""
        self._url = _url

        if status_code == 200:
            self.messages = messages
            self.see_also = see_also
            self.version = str(version)
            self.data_call_status = str(data_call_status)
            self.cached = bool(cached)
            self.data = data
            self.query_id = str(query_id)
            self.process_time = int(process_time)
            self.server_id = str(server_id)
            self.build_version = str(build_version)
            self.status = str(status)
            self.status_code = int(status_code)
            self.time = datetime.datetime.fromisoformat(time)
        else:
            raise ResponseError("Invalid response from API")


def get(path, params):
    """Retrieve the requested path with parameters as GET from the API."""

    url = API_URL + str(path) + "data.json?" + str(params)

    try:
        response = requests.get(url)
        response.raise_for_status()
        return Output(url, **response.json())
    except Exception as e:
        raise RequestError(e)
