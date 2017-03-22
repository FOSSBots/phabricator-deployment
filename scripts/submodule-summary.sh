#!/bin/bash
echo '|**module**|**tag**|**commit**|'
git submodule foreach -q 'tag=`git describe`; GIT_PAGER="less -E" git --no-pager log --pretty="| $path | $tag | {%h} |" -1'
