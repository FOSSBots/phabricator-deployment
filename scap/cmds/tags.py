import datetime
from string import Formatter
from context import execute

date_format="%Y-%m-%d"
tag_format="release/{date}/{sequence}"

def get_tags_by_date(today=datetime.datetime.today()):
    date = today.strftime(date_format)
    command = "git tag --list=release/%s/*" % date
    execute(command)

def make_tag():
    today = datetime.datetime.today()
    date = today.strftime(date_format)
    print(date)
    seq=1
    "git tag --list=release/%s/*" % date
    values={
        "date": date,
        "sequence": seq
    }
    formatter = Formatter()
    tag = formatter.vformat(tag_format, [], values)
    print(tag)

