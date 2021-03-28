import requests
import sys
import json
from pprint import pprint

from conduit import Conduit

phab = Conduit()

r = phab.request('maniphest.search', {'queryKey': sys.argv[1]})
data = r.data()
ids = [f"T{obj.id}" for obj in data]

url = 'https://gerrit.wikimedia.org/r/changes/'
for tid in ids:
  query = {'q': f"bug:{tid}"}

  res = requests.get(url, params=query)
  jsontxt = res.text[4:]
  objs = json.loads(jsontxt)
  for obj in objs:
    print(f"{tid},{obj['change_id']},-{obj['deletions']},+{obj['insertions']}")
