git submodule foreach -q 'tag=`git describe`; git log --pretty="| $path | %h | $tag | %<(40,trunc)%s |" -1'
