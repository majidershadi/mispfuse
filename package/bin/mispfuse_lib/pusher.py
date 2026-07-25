# The actual push. Both the command and the alert action build an Options,
# load a Template, open a MispClient and call push(). Grouping, attribute
# mapping, and keeping one bad event from sinking the batch all live here, so
# there's a single place to fix things instead of two.
import re

from pymisp import MISPEvent

_TOKEN = re.compile(r"\$([A-Za-z0-9_]+)\$")


class Options(object):
    # Push-time overrides. Anything left None falls back to the template.

    def __init__(self, grouping=None, group_field=None, event_info=None,
                 distribution=None, threat_level_id=None, analysis=None,
                 tags=None, to_ids=None, publish=None):
        self.grouping = grouping
        self.group_field = group_field
        self.event_info = event_info
        self.distribution = distribution
        self.threat_level_id = threat_level_id
        self.analysis = analysis
        self.tags = tags            # list or None
        self.to_ids = to_ids        # bool or None
        self.publish = publish      # bool or None


class Result(object):
    def __init__(self, ok, message, event_id=None, event_uuid=None, count=0):
        self.ok = ok
        self.message = message
        self.event_id = event_id
        self.event_uuid = event_uuid
        self.count = count


def push(records, template, client, options, logger):
    # Push the rows to MISP. Returns one Result per event we create. A single
    # event blowing up is captured, not raised, so the rest still go out.
    grouping = options.grouping or template.grouping
    results = []

    if grouping == "per_row":
        groups = [[r] for r in records]
    elif grouping == "by_field":
        field = options.group_field
        if not field:
            raise ValueError("grouping=by_field requires group_field.")
        groups = _group_by(records, field)
    else:  # single_event
        groups = [list(records)] if records else []

    for rows in groups:
        if not rows:
            continue
        results.append(_push_one(rows, template, client, options, logger))
    return results


def _group_by(records, field):
    ordered = {}
    for r in records:
        key = r.get(field, "")
        ordered.setdefault(key, []).append(r)
    return list(ordered.values())


def _push_one(rows, template, client, options, logger):
    # Build one event from a group of rows and send it.
    event = MISPEvent()
    event.info = _render(options.event_info or template.event_info, rows[0])
    event.distribution = _pick(options.distribution, template.distribution)
    event.threat_level_id = _pick(options.threat_level_id, template.threat_level_id)
    event.analysis = _pick(options.analysis, template.analysis)

    tags = options.tags if options.tags is not None else template.tags
    for tag in tags or []:
        event.add_tag(tag)

    default_to_ids = options.to_ids if options.to_ids is not None else template.default_to_ids

    added = 0
    for row in rows:
        for m in template.mappings:
            value = row.get(m.field)
            if value is None or value == "":
                continue
            warn = client.validate_mapping(m.type, m.category)
            if warn:
                if template.strict:
                    logger.warning("skipping (strict): %s", warn)
                    continue
                logger.warning("%s (pushing anyway; server is authority)", warn)
            to_ids = m.to_ids if m.to_ids is not None else default_to_ids
            comment = row.get(m.comment_field) if m.comment_field else None
            kwargs = {
                "value": value,
                "to_ids": to_ids,
                "disable_correlation": m.disable_correlation,
            }
            if m.type:
                kwargs["type"] = m.type
            if m.category:
                kwargs["category"] = m.category
            if comment:
                kwargs["comment"] = comment
            try:
                event.add_attribute(**kwargs)
                added += 1
            except Exception as exc:  # bad type/category for this value
                logger.warning("could not add attribute %s=%s: %s",
                               m.type or "auto", value, exc)

    if added == 0:
        return Result(False, "no mappable attributes in this group; nothing sent")

    publish = options.publish if options.publish is not None else template.publish
    event.published = bool(publish)

    try:
        created = client.add_event(event)
    except Exception as exc:
        logger.error("MISP add_event failed: %s", exc)
        return Result(False, "MISP add_event failed: {}".format(exc), count=added)

    eid = getattr(created, "id", None)
    euuid = getattr(created, "uuid", None)
    if eid is None:
        # server returned an error payload rather than an event
        return Result(False, "MISP rejected the event: {}".format(created), count=added)
    return Result(True, "event created", event_id=eid, event_uuid=euuid, count=added)


def _render(template_str, row):
    # Swap $field$ tokens in the event title for values from the row.
    if not template_str:
        return "IOCs from Splunk (MISPFuse)"
    return _TOKEN.sub(lambda mo: str(row.get(mo.group(1), mo.group(0))), template_str)


def _pick(override, fallback):
    return fallback if override is None else override
