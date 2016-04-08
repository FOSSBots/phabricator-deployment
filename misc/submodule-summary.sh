git submodule foreach -q 'tag=`git describe`; GIT_PAGER="less -E" git --no-pager log --pretty="| $path | %h | $tag | %<(40,trunc)%s |" -1'
