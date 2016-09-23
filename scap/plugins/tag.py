from __future__ import print_function, unicode_literals

import datetime
import logging
import sys
from scap import ansi, cli, log
from scap.utils import cd
from sh import git
from .asciitable import AsciiTable

submod = git.bake('submodule', 'foreach', '-q')

submodule_paths = []

def all_submodules():
    global submodule_paths
    if len(submodule_paths) < 1:
        submodule_paths = submod('echo $path').splitlines()
    for mod in submodule_paths:
        yield mod

def repo_plus_submodules():
    yield './'
    for mod in all_submodules():
        yield mod


@cli.command('tag', help='Manage release tags.', subcommands=False)

class ReleaseTagger(cli.Application):

    def _setup_loggers(self):
        """Setup logging."""
        log.setup_loggers(self.config, self.arguments.loglevel + 10)

    @cli.argument('-l','--list', dest='action', action='store_const',
                  const='list', help='List tags')
    @cli.argument('-c', dest='action', action='store_const', const='create',
                  help='Create new tag.')
    @cli.argument('--date', nargs=1, default=None, type=str, metavar='YYYY-MM-DD',
                  help="Specify the date for your tag, default: today's date")
    @cli.argument('-s', nargs=1, type=int, default=1, dest='seq', metavar='SEQ',
                  help='Sequence number: Increase this number when you tag\
                  more than one release on the same date.')
    @cli.argument('-m', dest='msg', metavar='TEXT', nargs='+', default='',
                  help='Commit message.')
    def main(self, *args):
        # print(self.arguments)
        action = getattr(self, self.arguments.action, False)
        if action:
            action()
        elif self.arguments.action == 'list':
            table = AsciiTable()
            table.header_row(('path', 'tag'))
            for path in repo_plus_submodules():
                with cd(path):
                    table.row([path, git('describe')])

            print(table.render())

    def create(self):
        date = self.arguments.date
        seq = self.arguments.seq
        msg = " ".join(self.arguments.msg)
        if (date is None):
            date=datetime.datetime.today()
            date_format="%Y-%m-%d"
            date = date.strftime(date_format)

        if len(date) != 10:
            raise ValueError('Date must be 10 digits, YYYY-MM-DD. You entered: %s' % date)

        if (type(seq) is not int):
            raise ValueError('Sequence must be numeric value > 0')

        tag_format="release/{date}/{seq}"

        tag = tag_format.format(date=date, seq=seq)
        print('Tagging repo and all submodules with new tag %s at HEAD' % tag)
        print('Tag annotation: %s' % msg)

        for path in repo_plus_submodules():
            with cd(path):
                git('tag', '-a', '-m', msg, tag)
