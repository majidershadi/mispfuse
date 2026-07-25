"""Group result rows, build MISP event payloads, and submit them."""
import re

_TOKEN = re.compile(r"\$([A-Za-z0-9_]+)\$")


class Options(object):
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
    """Push all groups and return one result for each attempted event."""
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
    """Build and submit one MISP event for a group of rows."""
    event = {
        "info": _render(options.event_info or template.event_info, rows[0]),
        "distribution": _pick(options.distribution, template.distribution),
        "threat_level_id": _pick(
            options.threat_level_id, template.threat_level_id
        ),
        "analysis": _pick(options.analysis, template.analysis),
        "published": bool(
            options.publish if options.publish is not None else template.publish
        ),
        "Attribute": [],
    }

    tags = options.tags if options.tags is not None else template.tags
    if tags:
        event["Tag"] = [{"name": tag} for tag in tags]

    default_to_ids = (
        options.to_ids if options.to_ids is not None else template.default_to_ids
    )

    for row in rows:
        for mapping in template.mappings:
            raw_value = row.get(mapping.field)
            values = _attribute_values(raw_value)
            if not values:
                continue
            warning = client.validate_mapping(mapping.type, mapping.category)
            if warning:
                if template.strict or not mapping.type:
                    logger.warning("skipping: %s", warning)
                    continue
                logger.warning("%s (sending; MISP remains authoritative)", warning)

            for value in values:
                attribute = {
                    "type": mapping.type,
                    "value": value,
                    "to_ids": (
                        mapping.to_ids
                        if mapping.to_ids is not None
                        else default_to_ids
                    ),
                    "disable_correlation": bool(mapping.disable_correlation),
                }
                if mapping.category:
                    attribute["category"] = mapping.category
                if mapping.comment_field and row.get(mapping.comment_field):
                    attribute["comment"] = str(row[mapping.comment_field])
                event["Attribute"].append(attribute)

    added = len(event["Attribute"])
    if added == 0:
        return Result(False, "no mappable attributes in this group; nothing sent")

    try:
        created = client.add_event(event)
    except Exception as exc:
        logger.error("MISP add_event failed: %s", exc)
        return Result(False, "MISP add_event failed: {}".format(exc), count=added)

    return Result(
        True,
        "event created",
        event_id=created.id,
        event_uuid=created.uuid,
        count=added,
    )

def _attribute_values(value):
    """Normalize Splunk scalar or multivalue fields into MISP strings."""
    if value is None or value == "":
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if item is not None and item != ""]
    return [str(value)]


def _render(template_str, row):
    if not template_str:
        return "IOCs from Splunk (MISPFuse)"
    return _TOKEN.sub(lambda mo: str(row.get(mo.group(1), mo.group(0))), template_str)


def _pick(override, fallback):
    return fallback if override is None else override
