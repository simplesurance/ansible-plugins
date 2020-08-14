# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

def target2region( value ):
    """
    Very simple filter plugin to extract region from the deployment target
    templated_string: "{{ target|target2region }}"
    """
    if re.search("^sb-.*", value):
        return "eu"

    x = re.search("^.+-(stg|prd)-(.+)$",value)
    if (x):
        return(x.group(2))

    return AnsibleFilterError("Cannot get region out of target: %s" % value)

def target2project_id( value ):
    """
    Very simple filter plugin to extract project_id from the deployment target
    templated_string: "{{ target|target2project_id }}"
    """
    if re.search("^sb-.*", value):
        return "sisu"

    x = re.search("^(.+)-(stg|prd)-(.+)$",value)
    if (x):
        return(x.group(1))

    return AnsibleFilterError("Cannot get project_id out of target: %s" % value)

class FilterModule(object):
    def filters(self):
        return {
            'target2region': target2region,
            'target2project_id': target2project_id,
        }
