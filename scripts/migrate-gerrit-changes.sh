#!/bin/bash
PROJECT="${1:-mediawiki/vagrant}"
APIURL="https://gerrit.wikimedia.org/r/changes/?q=status:open+project:$PROJECT&o=CURRENT_REVISION"
TMPFILE=$(mktemp)
curl $APIURL > $TMPFILE
tail --lines=+2 $TMPFILE | jq .
#rm $TMPFILE
