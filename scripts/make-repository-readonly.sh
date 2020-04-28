#!/bin/bash

# mark-repo-readonly.sh
# Marks all uris for a given diffusion repository as read-only.
# This script requires the following:
# 1. a working arcanist installed in your path as `arc`
# 2. the `jq` utility ( https://stedolan.github.io/jq/ ) also in your path.
#

notfound() {
  echo "Not found"
}

trap 'notfound' ERR

ARC=`which arcq`
echo $?
JQ=`which jq`

arc="arc call-conduit --conduit-uri https://phabricator.wikimedia.org/"
BASENAME=$0
BASENAME=$(basename $BASENAME)
if [ "$1" == "" ]
then

  echo "$BASENAME: Mark all uris for a given repository as read-only."
  echo ""
  echo "Usage: $BASENAME repo-short-name"
  exit 1
fi
QUERY="{ \"constraints\":  { \"shortNames\" : [ \"$1\" ] }, \"attachments\": { \"uris\": true } } "

JSON=$($arc diffusion.repository.search <<< "$QUERY")
IDS=$(jq -j '[.response.data[].attachments.uris.uris[] | select( .fields.io.effective == "readwrite") | .id] | join(" ")' <<< "$JSON")
URIS=$(jq -r  '.response.data[].attachments.uris.uris[] | select( .fields.io.effective == "readwrite") | [.id, .fields.uri.normalized ]|join(": ")' <<< "$JSON")
if [[ "$URIS" == "" ]]
then
  echo "No read/write URIs found for repo named $1."
  exit 1
fi
echo "Found the following writable URIs:"
echo
echo "$URIS"
echo
read -p "Mark these URIs read-only? " -n 1
if [[ $REPLY =~ ^[Yy]$ ]]
then
  set -e
  for ID in $IDS
  do
    echo
    echo -n "Marking URI $ID read-only..."
    $arc diffusion.uri.edit <<EOF
    {
       "transactions": [
          { "type": "io", "value": "read" }
        ], "objectIdentifier": "$ID"
    }
EOF
    echo -n
  done
  exit 0
fi
exit 1
