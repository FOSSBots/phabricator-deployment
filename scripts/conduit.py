from builtins import str

import json
import os
import re
import time
import sys
import requests
import pprint

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

class DataIterator(object):
    target = None
    def __init__(self, target):
        self.target = target.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        return Data(next(self.target))

class Data(object):
    data = None

    def __init__(self, data):
        self.data = data

    def __getattr__(self, attr):
        return self.data[attr]

    def __repr__(self):
        return pprint.saferepr(self.data)

    def __iter__(self):
        return DataIterator(self.data)

class Conduit(object):
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
                if (self.phab_url in arcrc['hosts']):
                    token = arcrc['hosts'][self.phab_url]['token']

        return os.environ.get('CONDUIT_TOKEN', token)

    def request(self, method, data):
        """
        Helper method to query phab via requests
        """
        data = flatten_for_post(data)
        data['api.token'] = self.conduit_token
        r = requests.post(f"{self.phab_url}{method}",data=data)
        return ConduitResult(conduit=self, res=r)


class ConduitResult(object):
    res = None
    _data = None
    conduit = None
    def __init__(self, conduit: Conduit, res: requests.Response):
        self.conduit = conduit
        self.res = res
        json = res.json()
        self._data = json['result']['data']


    def data(self):
        return Data(self._data)
