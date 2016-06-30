#!/usr/bin/env php
<?php
$next_deploy = date('Y-m-d', strtotime("+2 weeks"));
$tmpl = <<<TEMPLATE

== {icon book} [[ https://www.mediawiki.org/wiki/Phabricator/Maintenance | MediaWiki / Phabricator / Maintenance ]] ==
----

(NOTE) {icon exclamation-circle} Tasks solved upstream but still not deployed on phabricator.wikimedia.org should add this task as blocker. When there are significant / important blockers, @mmodell will pull from upstream and deploy during the soonest available deployment window. 


== {icon code-fork} Deployment Details:
TBD

== {icon chevron-circle-up} Upstream Changelog:
TBD

== {icon calendar} Event Details:
{E28}: This scheduled maintenance will occur between `1:00` and `2:00` (AM) UTC on $next_deploy.

----

== {icon subway} Other Deployments: ==

**Series Navigation:** 

| {icon chevron-left} |**Previous in this series**|{icon arrows-h}|**Next in this series**| {icon chevron-right} |
|
|| $prev_task | {icon arrows-h} | $next_task | |

{icon list} [[ /maniphest/query/9NgSV2wc1CGv/ | All Phabricator Deployments ]] 

TEMPLATE;
echo urlencode($tmpl);

