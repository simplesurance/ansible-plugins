from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import os.path
from pathlib import Path
from dotenv import dotenv_values

from ansible.errors import AnsibleError, AnsibleAssertionError
from ansible.parsing.splitter import parse_kv
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        basedir = self.get_basedir(variables)

        ret = []

        params = {
            'file': basedir + '/.env',
            'key': None,
        }

        for term in terms:
            kv = parse_kv(term)

            try:
                for name, value in kv.items():
                    if name not in params:
                        raise AnsibleAssertionError('%s not in params' % name)
                    params[name] = value
            except (ValueError, AssertionError) as e:
                raise AnsibleError(e)


            if not os.path.isfile(params['file']):
                raise FileNotFoundError

            dotenv = dotenv_values(dotenv_path=params['file'])
            data = json.dumps(dotenv)

            if key is None:
                ret.append(data)
            else:
                ret.append(data[key])

        return ret
