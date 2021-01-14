import json


def to_safe_json(value):
    """
    Safely escapes a json string and wraps it in double quotes.
    This is useful to use in deploy vars so that they can be safely passed
    as hcl environment variables.
    """
    return json.dumps(json.dumps(value))

def to_escaped_json(value):
    """
    Safely escapes a json string so that it can be wrapped in double quotes.
    This is useful to use in deploy vars so that they can be safely passed
    as hcl environment variables.
    The difference between `to_safe_json` and `to_escaped_json` is that
    `to_escaped_json` does NOT include the extra double quotes around the
    whole escaped json string.
    """
    return json.dumps(json.dumps(value))[1:-1]

class FilterModule(object):
    def filters(self):
        return {
            'to_safe_json': to_safe_json,
            'to_escaped_json': to_escaped_json,
        }
