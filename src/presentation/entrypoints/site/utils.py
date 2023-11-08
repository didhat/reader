import json
from enum import Enum
import datetime
import calendar


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return calendar.timegm(o.utctimetuple())

        if isinstance(o, (set, frozenset)):
            return list(o)

        if isinstance(o, Enum):
            return o.value

        return super().default(o)


def compact_json(pydict):
    return json.dumps(
        pydict, ensure_ascii=False, cls=JSONEncoder, separators=(",", ":")
    )


_js_escapes = {
    ord("\\"): "\\u005C",
    ord("'"): "\\u0027",
    ord('"'): "\\u0022",
    ord(">"): "\\u003E",
    ord("<"): "\\u003C",
    ord("&"): "\\u0026",
    ord("="): "\\u003D",
    ord("-"): "\\u002D",
    ord(";"): "\\u003B",
    ord("`"): "\\u0060",
    ord("\u2028"): "\\u2028",
    ord("\u2029"): "\\u2029",
}

# Escape every ASCII character with a value less than 32.
_js_escapes.update((ord("%c" % z), "\\u%04X" % z) for z in range(32))


def escapejs(value):
    """Hex encode characters for use in JavaScript strings."""
    return str(value).translate(_js_escapes)
