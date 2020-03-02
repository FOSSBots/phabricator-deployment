from builtins import str

import json
import os
import re
import time
import sys
import requests


URIS = {}


def flatten_for_post(h, result=None, kk=None):
    """
    Since phab expects x-url-encoded form post data (meaning each
    individual list element is named). AND because, evidently, requests
    can't do this for me, I found a solution via stackoverflow.

    See also:
    <https://secure.phabricator.com/T12447>
    <https://stackoverflow.com/questions/26266664/requests-form-urlencoded-data/36411923>
    """
    if result is None:
        result = {}

    if isinstance(h, str) or isinstance(h, bool):
        result[kk] = h
    elif isinstance(h, list) or isinstance(h, tuple):
        for i, v1 in enumerate(h):
            flatten_for_post(v1, result, '%s[%d]' % (kk, i))
    elif isinstance(h, dict):
        for (k, v) in h.items():
            key = k if kk is None else "%s[%s]" % (kk, k)
            if isinstance(v, dict):
                for i, v1 in v.items():
                    flatten_for_post(v1, result, '%s[%s]' % (key, i))
            else:
                flatten_for_post(v, result, key)
    return result


def replace_domain(uri):
    return re.sub(
        '^git@github.com:toolforge',
        'https://github.com/toolforge',
        uri
    )



class Phab(object):
    def __init__(self):
        self.phab_url = 'https://phabricator.wikimedia.org/api/'
        self.conduit_token = self._get_token()

    def _get_token(self):
        """
        Use the $CONDUIT_TOKEN envvar, fallback to whatever is in ~/.arcrc
        """
        token = None
        token_path = os.path.expanduser('~/.arcrc')
        if os.path.exists(token_path):
            with open(token_path) as f:
                arcrc = json.load(f)
                token = arcrc['hosts'][self.phab_url]['token']

        return os.environ.get('CONDUIT_TOKEN', token)

    def _query_phab(self, method, data):
        """
        Helper method to query phab via requests and return json
        """
        data = flatten_for_post(data)
        data['api.token'] = self.conduit_token
        r = requests.post(
            os.path.join(self.phab_url, method),
            data=data)
        r.raise_for_status()
        return r.json()

    def find_uris(self, after=None):
        """
        Find repository uris
        """
        data = {
                # "queryKey": "all",
                "queryKey": "active",
                "attachments": {
                    'uris': '1',
                },
            }

        if after:
            data['after'] = after

        repos = self._query_phab(
            'diffusion.repository.search',
            data
        )

        results = repos['result']

        if not results:
            return

        for repo in results['data']:
            for uri in repo['attachments']['uris']['uris']:
                # Looking only for uris that are pointing to github
                # that are also of io type "mirror"
                phid = uri['id']
                name = uri['fields']['uri']['raw']
                io  = uri['fields']['io']['raw']
                if 'git@github.com:toolforge' in name and io == 'mirror':
                    URIS[phid] = name

        after = results['cursor']['after']
        if after:
            self.find_uris(after)

        else:
            return

    def update_uri(self, phid, uri):
        method = 'diffusion.uri.edit'
        data = {
            'objectIdentifier': str(phid),
            'transactions': [{
                'type': 'uri',
                'value': str(uri)
            },
            {
                'type': 'credential',
                'value': 'PHID-CDTL-nmoe3padilhs4w6i3ptn'
            }]
        }
        print(flatten_for_post(data))
        # return {'error_code': None}
        return self._query_phab(method, data)


def main():
    p = Phab()
    phab_uri_path = 'phaburis.json'
    if not os.path.exists(phab_uri_path):
        p.find_uris()
        with open(phab_uri_path, 'w') as f:
            f.write(json.dumps(URIS))

    with open(phab_uri_path) as f:
        uris = json.loads(f.read())

    count = 0
    for phid, uri in uris.items():
        result = p.update_uri(phid, replace_domain(uri))
        if result['error_code']:
            print('OOOOHHHH NOOOO')
            print(result)
            sys.exit(1)
        count += 1
        if count >= 50:
            count = 0
            time.sleep(5)


if __name__ == '__main__':
    main()

