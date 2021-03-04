#!/bin/bash
git submodule foreach 'git push origin $(git describe --abbrev=0 --match=release*) wmf/stable || true'
tag=$(git describe --abbrev=0 --match=release*)
git push origin $tag wmf/stable
