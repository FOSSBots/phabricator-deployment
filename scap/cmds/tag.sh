#!/bin/bash

DATE=`date +%Y-%m-%d`
TAG="release/$DATE/1"
git submodule foreach "git tag -a $TAG -m 'Tagging for release'; git push origin $TAG"
