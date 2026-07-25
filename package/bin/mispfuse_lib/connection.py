"""MISP connection validation shared by the UCC account REST handler."""

from __future__ import annotations

import re
import ssl
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from urllib3 import exceptions as urllib3_exceptions

from mispfuse_lib.client import MispApiError, MispClient

CONNECT_TIMEOUT_SECONDS = 5.0
READ_TIMEOUT_SECONDS = 15.0
CONNECTION_TIMEOUT = (CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS)


class ConnectionTestError(Exception):
    """Connection error returned to the Configuration page."""


def normalize_misp_url(value: object) -> str:
    raw = str(value or '').strip()
    if not raw:
        raise ConnectionTestError('MISP URL is required.')
    try:
        parsed = urlsplit(raw)
        _ = parsed.port
    except ValueError as exc:
        raise ConnectionTestError('MISP URL contains an invalid port.') from exc
    if parsed.scheme.lower() not in ('http', 'https'):
        raise ConnectionTestError('MISP URL must use http:// or https://.')
    if not parsed.hostname:
        raise ConnectionTestError('MISP URL must include a hostname.')
    if parsed.username or parsed.password:
        raise ConnectionTestError(
            'MISP URL must not contain embedded usernames or passwords.'
        )
    if parsed.query or parsed.fragment:
        raise ConnectionTestError(
            'MISP URL must be a base URL without a query string or fragment.'
        )
    return urlunsplit(
        (parsed.scheme.lower(), parsed.netloc, parsed.path.rstrip('/'), '', '')
    )


def is_masked_secret(value: object) -> bool:
    text = str(value or '').strip()
    return len(text) >= 4 and all(character in ('*', '•') for character in text)


def as_bool(value: object, default: bool = False) -> bool:
    if value is None or str(value).strip() == '':
        return default
    return str(value).strip().lower() in ('1', 'true', 't', 'yes', 'y')


def resolve_account_values(
    payload: Mapping[str, Any], existing: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    current = dict(existing or {})
    raw_url = payload.get('misp_url')
    if raw_url is None or str(raw_url).strip() == '':
        raw_url = current.get('misp_url')
    url = normalize_misp_url(raw_url)

    raw_key = payload.get('misp_key')
    if raw_key is None or str(raw_key).strip() == '' or is_masked_secret(raw_key):
        raw_key = current.get('misp_key')
    key = str(raw_key or '').strip()
    if not key or is_masked_secret(key):
        raise ConnectionTestError('A valid MISP API key is required.')

    if 'verify_ssl' in payload and str(payload.get('verify_ssl', '')).strip() != '':
        verify_ssl = as_bool(payload.get('verify_ssl'), default=True)
    else:
        verify_ssl = as_bool(current.get('verify_ssl'), default=True)
    return {'misp_url': url, 'misp_key': key, 'verify_ssl': verify_ssl}


def _exception_chain(exc: BaseException):
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        current = current.__cause__ or current.__context__


def _contains_exception(exc: BaseException, classes: tuple[type[BaseException], ...]):
    return any(isinstance(item, classes) for item in _exception_chain(exc))


def _safe_detail(exc: BaseException, api_key: str) -> str:
    detail = ' '.join(str(item) for item in _exception_chain(exc) if str(item))
    if api_key:
        detail = detail.replace(api_key, '[REDACTED]')
    detail = re.sub(
        r'([a-zA-Z][a-zA-Z0-9+.-]*://)[^/@\s]+:[^/@\s]+@',
        r'\1[REDACTED]@',
        detail,
    )
    return re.sub(r'\s+', ' ', detail).strip()[:300]


def _classify_failure(exc: BaseException, url: str, api_key: str) -> ConnectionTestError:
    host = urlsplit(url).hostname or 'the configured host'
    if _contains_exception(exc, (urllib3_exceptions.SSLError, ssl.SSLError)):
        return ConnectionTestError(
            "TLS certificate verification failed for '{}'. Correct the certificate "
            'chain, or disable verification only for an isolated lab instance.'.format(
                host
            )
        )
    if _contains_exception(exc, (urllib3_exceptions.ProxyError,)):
        return ConnectionTestError(
            'The configured proxy could not connect to MISP. Verify the proxy host, '
            'port, protocol, and credentials.'
        )
    if _contains_exception(
        exc,
        (
            urllib3_exceptions.ConnectTimeoutError,
            urllib3_exceptions.ReadTimeoutError,
            urllib3_exceptions.TimeoutError,
        ),
    ):
        return ConnectionTestError(
            "Connection to '{}' timed out ({}s connect / {}s read).".format(
                host, CONNECT_TIMEOUT_SECONDS, READ_TIMEOUT_SECONDS
            )
        )
    if _contains_exception(
        exc,
        (
            urllib3_exceptions.NewConnectionError,
            urllib3_exceptions.MaxRetryError,
            urllib3_exceptions.ProtocolError,
        ),
    ):
        return ConnectionTestError(
            "Could not connect to '{}'. Verify DNS, routing, firewall rules, port, "
            'and proxy settings.'.format(host)
        )

    status = next(
        (item.status for item in _exception_chain(exc) if isinstance(item, MispApiError)),
        None,
    )
    if status in (401, 403):
        return ConnectionTestError(
            'MISP rejected the API key, or the key lacks permission to read its user.'
        )
    if status == 404:
        return ConnectionTestError(
            'The server was reached, but the MISP API endpoint was not found. '
            'Check the configured base URL and any MISP sub-path.'
        )

    detail = _safe_detail(exc, api_key)
    if detail:
        return ConnectionTestError('MISP connection test failed: {}'.format(detail))
    return ConnectionTestError("MISP connection test failed for '{}'.".format(host))


def test_misp_connection(
    url: str,
    api_key: str,
    verify_ssl: bool = True,
    proxies: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    normalized_url = normalize_misp_url(url)
    try:
        client = MispClient(
            normalized_url,
            api_key,
            verify_ssl=verify_ssl,
            proxies=dict(proxies or {}),
            timeout=CONNECTION_TIMEOUT,
        )
        result = client.test_connection()
    except Exception as exc:
        raise _classify_failure(exc, normalized_url, api_key) from exc
    return {
        'url': normalized_url,
        'version': result.get('version', 'unknown'),
        'type_count': result.get('type_count', 0),
    }
