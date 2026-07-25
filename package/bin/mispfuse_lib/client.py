# A small wrapper around PyMISP. It keeps the connection and the server's
# describeTypes, so we validate a template against the instance we're actually
# talking to instead of some list we baked in months ago. The server wins:
# validation only warns, so an admin can push a combination we wouldn't pick.
from pymisp import PyMISP

# Quiet the InsecureRequestWarning when someone turns off cert checking for a
# lab box. Don't touch the global warning filters.
try:
    import urllib3
except Exception:  # pragma: no cover
    urllib3 = None


class MispClient(object):
    def __init__(self, url, key, verify_ssl=True, proxies=None):
        if not verify_ssl and urllib3 is not None:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._misp = PyMISP(url, key, ssl=verify_ssl, proxies=proxies or {})
        self._types = None

    @property
    def taxonomy(self):
        # The server's describeTypes: types, categories,
        # category_type_mappings, sane_defaults. Fetched once, then cached.
        if self._types is None:
            self._types = self._misp.describe_types_remote
        return self._types

    def validate_mapping(self, type_, category):
        # Give back a warning string if this type/category won't fly on the
        # server, otherwise None. A bad combo never raises here.
        try:
            tax = self.taxonomy
        except Exception:
            # Couldn't reach describeTypes. Let the actual push say what's wrong.
            return None
        if type_ and type_ not in tax.get("types", []):
            return "type '{}' is not known to this MISP instance".format(type_)
        if type_ and category:
            allowed = tax.get("category_type_mappings", {}).get(category, [])
            if allowed and type_ not in allowed:
                return "type '{}' is not valid in category '{}' on this instance".format(
                    type_, category
                )
        return None

    def add_event(self, event):
        return self._misp.add_event(event, pythonify=True)
