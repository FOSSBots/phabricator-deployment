#!/bin/bash
TAGDATE=`date +%Y-%m-%d`
DEFAULTREV=1
REV=${2-$DEFAULTREV}
TAGDATE=${1-$TAGDATE}
TAG="release/$TAGDATE/$REV"
git submodule foreach "git tag -d $TAG" > /dev/null 2>&1
TAGCMD="git tag -a $TAG -m \"tagging $TAG\""
git submodule foreach "$TAGCMD"
git tag -d $TAG >/dev/null 2>&1
git tag -a $TAG -m "tagging for release: $TAG"
git submodule foreach --quiet 'git describe'
git describe

scap tag milestone --project Phabricator --template ./templates/phab.tmpl $TAGDATE
