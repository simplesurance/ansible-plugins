import json
import os.path
from dotenv import dotenv_values

from ansible.errors import AnsibleError, AnsibleAssertionError
from ansible.parsing.splitter import parse_kv
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        ret = []

        params = {
            'file': '.env',
            'path': self.get_basedir(variables),
            'key': None,
        }

        for term in terms:
            kv = parse_kv(term)

            try:
                for name, value in kv.items():
                    if name not in params:
                        raise AnsibleAssertionError('{} not in params'.format(name))
                    params[name] = value
            except (ValueError, AssertionError) as e:
                raise AnsibleError(e)

            path = params['file']
            if params['path']:
                path = '{}/{}'.format(params['path'], params['file'])

            if not os.path.isfile(path):
                raise FileNotFoundError

            dotenv = dotenv_values(dotenv_path=path)
            data = json.loads(json.dumps(dotenv))

            if params['key'] is None:
                ret.append(data)
            else:
                try:
                    ret.append(data[params['key']])
                except (KeyError) as e:
                    raise AnsibleError(e)

        return ret
