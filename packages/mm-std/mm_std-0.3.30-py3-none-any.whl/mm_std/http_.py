import json
from dataclasses import asdict, dataclass, field
from typing import Any, cast
from urllib.parse import urlencode, urlparse

import aiohttp
import pydash
import requests
from aiohttp_socks import ProxyConnector
from multidict import CIMultiDictProxy
from requests.auth import AuthBase

from mm_std.result import Err, Ok, Result

FIREFOX_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0"
SAFARI_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15"
)
CHROME_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


@dataclass
class HResponse:
    code: int = 0
    error: str | None = None
    body: str = ""
    headers: dict[str, str] = field(default_factory=dict)

    _json_data: Any = None
    _json_parsed = False
    _json_parsed_error = False

    def _parse_json(self) -> None:
        try:
            self._json_data = None
            self._json_data = json.loads(self.body)
            self._json_parsed_error = False
        except json.JSONDecodeError:
            self._json_parsed_error = True
        self._json_parsed = True

    @property
    def json(self) -> Any:  # noqa: ANN401
        if not self._json_parsed:
            self._parse_json()
        return self._json_data

    @property
    def json_parse_error(self) -> bool:
        if not self._json_parsed:
            self._parse_json()
        return self._json_parsed_error

    @property
    def content_type(self) -> str | None:
        for key in self.headers:
            if key.lower() == "content-type":
                return self.headers[key]
        return None

    def to_err_result[T](self, error: str | None = None) -> Err:
        return Err(error or self.error or "error", data=asdict(self))

    def to_ok_result[T](self, result: T) -> Result[T]:
        return Ok(result, data=asdict(self))

    def is_error(self) -> bool:
        return self.error is not None

    def is_timeout_error(self) -> bool:
        return self.error == "timeout"

    def is_proxy_error(self) -> bool:
        return self.error == "proxy"

    def is_connection_error(self) -> bool:
        return self.error is not None and self.error.startswith("connection:")

    def is_dns_error(self) -> bool:
        return self.error is not None and self.error.startswith("dns:")

    def to_dict(self) -> dict[str, Any]:
        return pydash.omit(asdict(self), "_json_data")


def hrequest(
    url: str,
    *,
    method: str = "GET",
    proxy: str | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: float = 10,
    user_agent: str | None = None,
    json_params: bool = True,
    auth: AuthBase | tuple[str, str] | None = None,
    verify: bool = True,
) -> HResponse:
    query_params: dict[str, Any] | None = None
    data: dict[str, Any] | None = None
    json_: dict[str, Any] | None = None
    method = method.upper()
    if not headers:
        headers = {}
    if user_agent:
        headers["user-agent"] = user_agent
    if method == "GET":
        query_params = params
    elif json_params:
        json_ = params
    else:
        data = params

    proxies = None
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy,
        }

    try:
        r = requests.request(
            method,
            url,
            proxies=proxies,
            timeout=timeout,
            cookies=cookies,
            auth=auth,
            verify=verify,
            headers=headers,
            params=query_params,
            json=json_,
            data=data,
        )
        return HResponse(code=r.status_code, body=r.text, headers=dict(r.headers))
    except requests.exceptions.Timeout:
        return HResponse(error="timeout")
    except requests.exceptions.ProxyError:
        return HResponse(error="proxy")
    except requests.exceptions.RequestException as err:
        return HResponse(error=f"connection: {err}")
    except Exception as err:
        return HResponse(error=f"exception: {err}")


async def hrequest_async(
    url: str,
    *,
    method: str = "GET",
    proxy: str | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
    cookies: dict[str, Any] | None = None,
    timeout: float = 10,
    user_agent: str | None = None,
    json_params: bool = True,
    auth: tuple[str, str] | None = None,
) -> HResponse:
    query_params: dict[str, Any] | None = None
    data: dict[str, Any] | None = None
    json_: dict[str, Any] | None = None
    method = method.upper()

    if not headers:
        headers = {}
    if user_agent:
        headers["user-agent"] = user_agent
    if method == "GET":
        query_params = params
    elif json_params:
        json_ = params
    else:
        data = params

    try:
        request_kwargs: dict[str, Any] = {"headers": headers}
        if query_params:
            request_kwargs["params"] = query_params
        if json_:
            request_kwargs["json"] = json_
        if data:
            request_kwargs["data"] = data
        if cookies:
            request_kwargs["cookies"] = cookies
        if auth and isinstance(auth, tuple) and len(auth) == 2:
            request_kwargs["auth"] = aiohttp.BasicAuth(auth[0], auth[1])

        if proxy and proxy.startswith("socks"):
            return await _aiohttp_socks5(url, method, proxy, request_kwargs, timeout)
        return await _aiohttp(url, method, request_kwargs, timeout=timeout, proxy=proxy)

    except TimeoutError:
        return HResponse(error="timeout")
    except (aiohttp.ClientProxyConnectionError, aiohttp.ClientHttpProxyError, aiohttp.ClientConnectorError) as err:
        if is_proxy_error(str(err), proxy):
            return HResponse(error="proxy")
        return HResponse(error=f"connection: {err}")
    except aiohttp.ClientError as err:
        return HResponse(error=f"error: {err}")
    except Exception as err:
        return HResponse(error=f"exception: {err}")


def is_proxy_error(error_message: str, proxy: str | None) -> bool:
    if not proxy:
        return False
    error_message = error_message.lower()
    if "proxy" in error_message:
        return True
    return bool("cannot connect to" in error_message and cast(str, urlparse(proxy).hostname) in error_message)


async def _aiohttp(
    url: str, method: str, request_kwargs: dict[str, object], timeout: float | None = None, proxy: str | None = None
) -> HResponse:
    if proxy:
        request_kwargs["proxy"] = proxy
    client_timeout = aiohttp.ClientTimeout(total=timeout) if timeout else None
    async with aiohttp.ClientSession(timeout=client_timeout) as session, session.request(method, url, **request_kwargs) as res:  # type: ignore[arg-type]
        return HResponse(code=res.status, body=await res.text(), headers=headers_dict(res.headers))


async def _aiohttp_socks5(
    url: str, method: str, proxy: str, request_kwargs: dict[str, object], timeout: float | None = None
) -> HResponse:
    connector = ProxyConnector.from_url(proxy)
    client_timeout = aiohttp.ClientTimeout(total=timeout) if timeout else None
    async with (
        aiohttp.ClientSession(connector=connector, timeout=client_timeout) as session,
        session.request(method, url, **request_kwargs) as res,  # type: ignore[arg-type]
    ):
        return HResponse(code=res.status, body=await res.text(), headers=headers_dict(res.headers))


def add_query_params_to_url(url: str, params: dict[str, object]) -> str:
    query_params = urlencode({k: v for k, v in params.items() if v is not None})
    if query_params:
        url += f"?{query_params}"
    return url


hr = hrequest
hra = hrequest_async


def headers_dict(headers: CIMultiDictProxy[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key in headers:
        values = headers.getall(key)
        if len(values) == 1:
            result[key] = values[0]
        else:
            result[key] = ", ".join(values)
    return result
