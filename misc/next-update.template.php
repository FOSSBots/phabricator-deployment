#!/usr/bin/env php
<?php
$next_deploy = date('Y-m-d', strtotime("+2 weeks"));
$tmpl = <<<TEMPLATE
{icon book} [[ https://www.mediawiki.org/wiki/Phabricator/Maintenance | MediaWiki / Phabricator / Maintenance ]]

{icon calendar} Event: {E28} Wednesday, $next_deploy @ Midnight UTC

(NOTE) Tasks solved upstream but still not deployed on phabricator.wikimedia.org should add this task as blocker.

{icon subway} Other Deployments:

| Previous | Next |
|{icon chevron-left} {T106645} |  **`None scheduled`** {icon chevron-right} |

TEMPLATE;
echo urlencode($tmpl);

