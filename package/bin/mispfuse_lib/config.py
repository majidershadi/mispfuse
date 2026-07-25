# Reads the config the UI writes: accounts, proxy, logging.
# The API key lives encrypted in storage/passwords, never in a .conf and
# never in a keys.py. ConfManager hands it back decrypted as long as the
# realm matches what UCC uses:
#     __REST_CREDENTIAL__#<AppName>#configs/conf-<restRoot>_account
import logging

from solnlib import conf_manager

from mispfuse_lib import APP_NAME, REST_ROOT

ACCOUNT_CONF = "{}_account".format(REST_ROOT)
SETTINGS_CONF = "{}_settings".format(REST_ROOT)
CRED_REALM = "__REST_CREDENTIAL__#{}#configs/conf-{}".format(APP_NAME, ACCOUNT_CONF)


class ConfigError(Exception):
    pass


def get_account(session_key, account_name):
    # Returns {misp_url, misp_key, verify_ssl} for one instance, key decrypted.
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
    # requests-style proxies dict, or {} when proxy is off/unset.
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
    auth = "{}:{}@".format(user, pwd) if user and pwd else ""
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
