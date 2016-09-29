# This Python file uses the following encoding: utf-8

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

def trunc(len, string, ellipsis=" …"):
    return string[0:len] + ellipsis

def action_arg(*args, **kwargs):
    kwargs['const'] = kwargs['action']
    kwargs['dest'] = 'action'
    kwargs['action'] ='store_const'
    kwargs['metavar'] = 'ACTION'
    return cli.argument(*args, **kwargs)


@cli.command('tag', subcommands=True)
@cli.argument('-h', '--help', action='help')
class ReleaseTagger(cli.Application):
    """
    Manage release tags in this repository plus each of it's submodules.
    """
    action = None

    def _setup_loggers(self):
        """Setup logging."""
        log.setup_loggers(self.config, self.arguments.loglevel + 10)


    def _process_arguments(self, args, extra_args):
        #print(args,extra_args)
        return args,extra_args

    #@cli.argument('-l', help='list tags', action='store_true')

    @cli.subcommand()
    def list(self, *args):
        ''' list the most recent tag in this repo plus all submodules '''
        table = AsciiTable()
        table.header_row(('path', 'branch', 'tag', 'commit'))
        for path in repo_plus_submodules():
            with cd(path):
                sha1 = git('rev-parse', 'HEAD')
                branch = git('symbolic-ref', '--short', 'HEAD')
                desc = git('describe')
                table.row([path, branch, desc, trunc(10, sha1.stdout)])
        print(table.render())

    @cli.argument('msg', metavar='TEXT', nargs='?', default='',
                  help='Tag Annotation / Commit message.')
    @cli.argument('--date', nargs=1, default=None, type=str, metavar='YYYY-MM-DD',
                help="Specify the date for your tag, default: today's date")
    @cli.argument('-s', nargs=1, type=int, default=1, dest='seq', metavar='SEQ',
                help='Sequence number: Increase this number when you tag\
                more than one release on the same date.')
    @cli.argument('-f', '--force', action='store_true',
                  help='Continue operation ignoring any errors.')
    def create(self, *args):
        ''' create a tag in this repo plus all submodules '''
        tag, date, seq = self.get_calver_tag()

        if len(self.arguments.msg):
            msg = " ".join(self.arguments.msg)
        else:
            msg = "Release tag #%s for %s" % (seq, date)

        print('Tagging repository + all submodules at HEAD -> %s' % tag)
        print('Tag annotation: "%s"' % msg)

        for path in repo_plus_submodules():
            with cd(path):
                try:
                    git('tag', '-a', '-m', msg, tag)
                    print(git('describe'))
                except Exception as ex:
                    if self.arguments.force:
                        print(ex)
                    else:
                        raise ex

    @cli.argument('--date', nargs=1, default=None, type=str, metavar='YYYY-MM-DD',
                help="Specify the date for your tag, default: today's date")
    @cli.argument('-s', nargs=1, type=int, default=1, dest='seq', metavar='SEQ',
                help='Sequence number: Increase this number when you tag\
                more than one release on the same date.')
    @cli.argument('-f', '--force', action='store_true',
                  help='Continue operation ignoring any errors.')
    def delete(self, *args):
        ''' delete tag in this repo plus all submodules '''
        tag,date,seq = self.get_calver_tag()
        for path in repo_plus_submodules():
            with cd(path):
                print(git('tag','-d', tag))

    def get_calver_tag(self):
        ''' generate a tag string with the format release/{date}/{sequence} '''
        date = self.arguments.date
        seq = self.arguments.seq

        if (date is None):
            date=datetime.datetime.today()
            date_format="%Y-%m-%d"
            date = date.strftime(date_format)
        else:
            date=date[0]
        if len(date) != 10:
            raise ValueError('Date must be 10 digits, YYYY-MM-DD. You entered: %s' % date)

        if (type(seq) is not int):
            raise ValueError('Sequence must be numeric value > 0')

        tag_format="release/{date}/{seq}"

        return (tag_format.format(date=date, seq=seq), date, seq)
