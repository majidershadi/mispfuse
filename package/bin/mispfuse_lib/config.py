"""Read MISPFuse account, proxy, and logging settings."""
import logging
from urllib.parse import quote

from solnlib import conf_manager

from mispfuse_lib import APP_NAME, REST_ROOT

ACCOUNT_CONF = "{}_account".format(REST_ROOT)
SETTINGS_CONF = "{}_settings".format(REST_ROOT)
CRED_REALM = "__REST_CREDENTIAL__#{}#configs/conf-{}".format(APP_NAME, ACCOUNT_CONF)


class ConfigError(Exception):
    pass


def get_account(session_key, account_name):
    """Return the URL, decrypted API key, and TLS setting for an account."""
    if not account_name:
        raise ConfigError("No MISP instance (account) was specified.")
    cfm = conf_manager.ConfManager(session_key, APP_NAME, realm=CRED_REALM)
    try:
        conf = cfm.get_conf(ACCOUNT_CONF)
        stanza = conf.get(account_name)
    except conf_manager.ConfManagerException as exc:
        raise ConfigError(
            "MISP instance '{}' not found. Configure it under "
            "Configuration > MISP Instances. ({})".format(account_name, exc)
        ) from exc
    if stanza is None:
        raise ConfigError(
            "MISP instance '{}' not found. Configure it under "
            "Configuration > MISP Instances.".format(account_name)
        )
    url = (stanza.get("misp_url") or "").strip().rstrip("/")
    key = (stanza.get("misp_key") or "").strip()
    if not url or not key:
        raise ConfigError(
            "MISP instance '{}' is missing a URL or API key.".format(account_name)
        )
    return {
        "misp_url": url,
        "misp_key": key,
        "verify_ssl": _as_bool(stanza.get("verify_ssl"), default=True),
    }


def get_proxies(session_key):
    """Return proxy URLs for urllib3, or an empty mapping."""
    cfm = conf_manager.ConfManager(session_key, APP_NAME)
    try:
        settings = cfm.get_conf(SETTINGS_CONF).get_all()
    except conf_manager.ConfManagerException:
        return {}
    proxy = settings.get("proxy", {})
    if not _as_bool(proxy.get("proxy_enabled"), default=False):
        return {}
    host = proxy.get("proxy_url")
    port = proxy.get("proxy_port")
    if not host or not port:
        return {}
    user = proxy.get("proxy_username")
    pwd = proxy.get("proxy_password")
    scheme = (proxy.get("proxy_type") or "http").lower()
    auth = ""
    if user and pwd:
        auth = "{}:{}@".format(quote(str(user), safe=""), quote(str(pwd), safe=""))
    uri = "{}://{}{}:{}".format(scheme, auth, host, port)
    return {"http": uri, "https": uri}


def get_log_level(session_key):
    cfm = conf_manager.ConfManager(session_key, APP_NAME)
    try:
        settings = cfm.get_conf(SETTINGS_CONF).get_all()
        return settings.get("logging", {}).get("loglevel", "INFO")
    except conf_manager.ConfManagerException:
        return "INFO"


def _as_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "t", "yes", "y")


def get_logger(name, session_key=None):
    logger = logging.getLogger(name)
    if session_key is not None:
        try:
            logger.setLevel(get_log_level(session_key))
        except Exception:
            logger.setLevel(logging.INFO)
    return logger
