# Templates are stanzas in mispfuse_templates.conf. Each one holds the
# event-level defaults and a list of field->attribute mappings. This is where
# people customise how a Splunk field turns into a MISP attribute; they edit
# the conf, not the code.
#
# A mapping line (map.1, map.2, ...) looks like:
#     map.N = field:type:category:to_ids:disable_correlation[:comment_field]
# Leave type/category empty and MISP picks a sane default for the value.
# to_ids empty means "use the template/option default"; disable_correlation
# empty means 0; comment_field is an optional field to pull a comment from.
from solnlib import conf_manager

from mispfuse_lib import APP_NAME, REST_ROOT

TEMPLATES_CONF = "{}_templates".format(REST_ROOT)


class TemplateError(Exception):
    pass


class Mapping(object):
    __slots__ = ("field", "type", "category", "to_ids",
                 "disable_correlation", "comment_field")

    def __init__(self, field, type_, category, to_ids,
                 disable_correlation, comment_field):
        self.field = field
        self.type = type_ or None
        self.category = category or None
        self.to_ids = to_ids
        self.disable_correlation = disable_correlation
        self.comment_field = comment_field or None


class Template(object):
    def __init__(self, name, stanza):
        self.name = name
        self.grouping = (stanza.get("grouping") or "single_event").strip()
        self.event_info = stanza.get("event_info") or "IOCs from Splunk (MISPFuse)"
        self.distribution = _int(stanza.get("distribution"), 0)
        self.threat_level_id = _int(stanza.get("threat_level_id"), 4)
        self.analysis = _int(stanza.get("analysis"), 0)
        self.publish = _bool(stanza.get("publish"), False)
        self.strict = _bool(stanza.get("strict"), False)
        self.default_to_ids = _bool(stanza.get("to_ids"), False)
        self.tags = [t.strip() for t in (stanza.get("tags") or "").split(",") if t.strip()]
        self.mappings = self._parse_mappings(stanza)
        if not self.mappings:
            raise TemplateError(
                "Template '{}' has no map.* mappings defined.".format(name)
            )

    def _parse_mappings(self, stanza):
        mappings = []
        for key in sorted(k for k in stanza if k.startswith("map.")):
            raw = stanza.get(key, "")
            parts = [p.strip() for p in raw.split(":")]
            if not parts or not parts[0]:
                continue
            field = parts[0]
            type_ = parts[1] if len(parts) > 1 else ""
            category = parts[2] if len(parts) > 2 else ""
            to_ids = _tri(parts[3]) if len(parts) > 3 else None
            disable_corr = _bool(parts[4], False) if len(parts) > 4 else False
            comment_field = parts[5] if len(parts) > 5 else ""
            mappings.append(
                Mapping(field, type_, category, to_ids, disable_corr, comment_field)
            )
        return mappings


def load_template(session_key, name):
    cfm = conf_manager.ConfManager(session_key, APP_NAME)
    try:
        conf = cfm.get_conf(TEMPLATES_CONF)
        stanza = conf.get(name)
    except conf_manager.ConfManagerException as exc:
        raise TemplateError(
            "Template '{}' not found in {}.conf ({}).".format(
                name, TEMPLATES_CONF, exc
            )
        )
    return Template(name, stanza)


def _int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool(value, default):
    if value is None or value == "":
        return default
    return str(value).strip().lower() in ("1", "true", "t", "yes", "y")


def _tri(value):
    """Three-state: None when unset, else bool."""
    if value is None or value == "":
        return None
    return str(value).strip().lower() in ("1", "true", "t", "yes", "y")
