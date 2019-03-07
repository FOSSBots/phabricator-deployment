#!/bin/bash
git diff --quiet || 

TAGDATE=`date +%Y-%m-%d -u`
DEFAULTREV=1
REV=${2-$DEFAULTREV}
TAGDATE=${1-$TAGDATE}
TAG="release/$TAGDATE/$REV"
git submodule foreach "git tag -d $TAG" > /dev/null 2>&1
MSG="phabricator.wikimedia.org version $TAG"
TAGCMD="git tag -a $TAG --sign -m \"$MSG\""
git submodule foreach "$TAGCMD"
git tag -d $TAG >/dev/null 2>&1
git tag -a $TAG --sign -m "$MSG"
git submodule foreach --quiet 'git describe'
git describe

git push origin wmf/stable $TAG
git submodule foreach "git push origin wmf/stable +$TAG"

scap tag milestone --project phabricator --template ./templates/phab.tmpl $TAGDATE
