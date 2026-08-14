"""HTTP client for the MISP endpoints used by MISPFuse."""

from __future__ import annotations

import json
import ssl
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlsplit

import urllib3
from urllib3.exceptions import HTTPError

MAX_RESPONSE_BYTES = 8 * 1024 * 1024
DEFAULT_CONNECT_TIMEOUT = 5.0
DEFAULT_READ_TIMEOUT = 30.0


class MispApiError(Exception):
    """MISP transport, HTTP, or response-format failure."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class CreatedEvent:
    id: str
    uuid: str | None
    raw: Mapping[str, Any]


class MispClient:
    def __init__(
        self,
        url: str,
        key: str,
        verify_ssl: bool = True,
        proxies: Mapping[str, str] | None = None,
        timeout: tuple[float, float] | None = None,
    ) -> None:
        self._url = url.rstrip('/')
        self._key = key
        self._verify_ssl = bool(verify_ssl)
        self._types: dict[str, Any] | None = None
        connect, read = timeout or (
            DEFAULT_CONNECT_TIMEOUT,
            DEFAULT_READ_TIMEOUT,
        )
        self._timeout = urllib3.Timeout(connect=float(connect), read=float(read))
        self._http = self._make_manager(dict(proxies or {}))

    def _make_manager(self, proxies: dict[str, str]):
        context = ssl.create_default_context()
        if not self._verify_ssl:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        scheme = urlsplit(self._url).scheme.lower()
        proxy_url = proxies.get(scheme) or proxies.get('https') or proxies.get('http')
        common = {
            'ssl_context': context,
            'timeout': self._timeout,
            'retries': False,
        }
        if not proxy_url:
            return urllib3.PoolManager(**common)

        proxy_scheme = urlsplit(proxy_url).scheme.lower()
        if proxy_scheme.startswith('socks'):
            from urllib3.contrib.socks import SOCKSProxyManager

            return SOCKSProxyManager(proxy_url, **common)
        return urllib3.ProxyManager(proxy_url, **common)

    @property
    def taxonomy(self) -> dict[str, Any]:
        if self._types is None:
            data = self._request('GET', 'attributes/describeTypes.json')
            self._types = _normalize_describe_types(data)
        return self._types

    def validate_mapping(self, type_: str | None, category: str | None) -> str | None:
        if not type_:
            return 'mapping has no MISP attribute type'
        tax = self.taxonomy
        if type_ not in tax.get('types', []):
            return "type '{}' is not known to this MISP instance".format(type_)
        if category:
            categories = tax.get('categories', [])
            if categories and category not in categories:
                return "category '{}' is not known to this MISP instance".format(category)
            allowed = tax.get('category_type_mappings', {}).get(category, [])
            if allowed and type_ not in allowed:
                return "type '{}' is not valid in category '{}' on this instance".format(
                    type_, category
                )
        return None

    def test_connection(self) -> dict[str, Any]:
        version_data = self._request('GET', 'servers/getVersion')
        user_data = self._request('GET', 'users/view/me')
        taxonomy = self.taxonomy

        if not isinstance(version_data, dict) or not version_data.get('version'):
            raise MispApiError('MISP did not return a server version.')
        if not isinstance(user_data, dict) or not isinstance(user_data.get('User'), dict):
            raise MispApiError('MISP did not return the authenticated user.')
        return {
            'version': str(version_data['version']),
            'type_count': len(taxonomy['types']),
        }

    def add_event(self, event: Mapping[str, Any]) -> CreatedEvent:
        response = self._request('POST', 'events/add', {'Event': dict(event)})
        if not isinstance(response, dict):
            raise MispApiError('MISP returned an invalid event-creation response.')
        event_data = response.get('Event', response)
        if not isinstance(event_data, dict):
            raise MispApiError('MISP returned an invalid event object.')
        event_id = event_data.get('id')
        if event_id in (None, ''):
            raise MispApiError(_extract_message(response) or 'MISP rejected the event.')
        return CreatedEvent(
            id=str(event_id),
            uuid=str(event_data['uuid']) if event_data.get('uuid') else None,
            raw=event_data,
        )

    def _request(
        self,
        method: str,
        path: str,
        payload: Mapping[str, Any] | None = None,
    ) -> Any:
        url = '{}/{}'.format(self._url, path.lstrip('/'))
        body = None
        if payload is not None:
            body = json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode(
                'utf-8'
            )
        headers = {
            'Authorization': self._key,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            # Limit response size before decoding JSON.
            'Accept-Encoding': 'identity',
            'User-Agent': 'MISPFuse/2.2.2',
        }

        response = None
        try:
            response = self._http.request(
                method,
                url,
                body=body,
                headers=headers,
                timeout=self._timeout,
                retries=False,
                redirect=False,
                preload_content=False,
                decode_content=False,
            )
            raw = response.read(MAX_RESPONSE_BYTES + 1, decode_content=False)
        except HTTPError:
            raise
        finally:
            if response is not None:
                # Do not return a partially read connection to the pool.
                try:
                    response.close()
                finally:
                    response.release_conn()

        if len(raw) > MAX_RESPONSE_BYTES:
            raise MispApiError('MISP response exceeded the 8 MiB safety limit.')

        data: Any = None
        if raw:
            try:
                data = json.loads(raw.decode('utf-8'))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise MispApiError(
                    'MISP returned a non-JSON response (HTTP {}).'.format(response.status),
                    status=int(response.status),
                ) from exc

        status = int(response.status)
        if status < 200 or status >= 300:
            message = _extract_message(data) or 'MISP API request failed.'
            raise MispApiError(
                'HTTP {}: {}'.format(status, message),
                status=status,
            )
        return data


def _normalize_describe_types(value: Any) -> dict[str, Any]:
    """Accept current MISP and legacy describeTypes response envelopes."""

    data = value
    if isinstance(data, dict) and isinstance(data.get('result'), dict):
        data = data['result']

    if not isinstance(data, dict) or not isinstance(data.get('types'), list):
        raise MispApiError(
            'MISP returned an invalid describeTypes response: expected '
            'a types list at result.types or types.'
        )

    normalized = dict(data)
    normalized.setdefault('categories', [])
    normalized.setdefault('category_type_mappings', {})
    normalized.setdefault('sane_defaults', {})
    return normalized


def _extract_message(value: Any) -> str | None:
    if isinstance(value, str):
        return value[:300]
    if isinstance(value, list):
        for item in value:
            message = _extract_message(item)
            if message:
                return message
        return None
    if isinstance(value, dict):
        for key in ('message', 'name', 'error', 'errors', 'reason'):
            if key in value:
                message = _extract_message(value[key])
                if message:
                    return message
    return None
