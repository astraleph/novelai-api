from novelai_api._low_level import Low_Level
from novelai_api._high_level import High_Level

from http.cookies import SimpleCookie
from aiohttp import ClientSession, ClientTimeout
from multidict import CIMultiDict

from logging import Logger
from typing import NoReturn, Optional

from os.path import dirname, abspath


class NovelAI_API:
    # Constants
    BASE_ADDRESS: str = "https://api.novelai.net"

    # Variables
    _logger: Logger
    _session: Optional[ClientSession]

    _lib_root: str = dirname(abspath(__file__))

    _timeout: ClientTimeout
    headers: CIMultiDict
    cookies: SimpleCookie

    low_level: Low_Level
    high_level: High_Level

    def __init__(self, session: Optional[ClientSession] = None, logger: Optional[Logger] = None):
        # variable passing
        assert session is None or type(session) is ClientSession, \
            f"Expected None or type 'ClientSession' for session, but got type '{type(session)}'"

        # no session = synchronous
        self._logger = Logger("NovelAI_API") if logger is None else logger
        self._session = session

        self._timeout = ClientTimeout(300)
        self.headers = CIMultiDict()
        self.cookies = SimpleCookie()

        # API parts
        self.low_level = Low_Level(self)
        self.high_level = High_Level(self)

    def attach_session(self, session: ClientSession) -> NoReturn:
        """
        Attach a ClientSession, making the requests asynchronous
        """

        assert type(session) is ClientSession, f"Expected type 'ClientSession' for session, but got type '{type(session)}'"

        self._session = session

    def detach_session(self) -> NoReturn:
        """
        Detach the current ClientSession, making the requests synchronous
        """

        self._session = None

    @property
    def timeout(self) -> float:
        """
        Timeout for a request (in seconds)
        """

        return self._timeout.total

    @timeout.setter
    def timeout(self, value: float) -> NoReturn:
        """
        Timeout for a request (in seconds)
        """

        self._timeout = ClientTimeout(value)
