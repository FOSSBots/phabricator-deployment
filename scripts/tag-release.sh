#!/bin/bash
TAGDATE=`date +%Y-%m-%d`
REV=1
TAGDATE=${1-$TAGDATE}
TAG="release/$TAGDATE/$REV"
git submodule foreach "git tag -d $TAG" > /dev/null 2>&1
TAGCMD="git tag -a $TAG -m \"tagging $TAG\""
git submodule foreach "$TAGCMD"
git tag -d $TAG >/dev/null 2>&1
git tag -a $TAG -m "tagging for release: $TAG"
git submodule foreach --quiet 'git describe'
git describe
