# This Python file uses the following encoding: utf-8

from __future__ import print_function, unicode_literals
import attr
from scap import ansi

@attr.s
class RowStyle(object):
    text_style = attr.ib(default=ansi.esc(ansi.FG_WHITE, ansi.BRIGHT))
    border_style = attr.ib(default=ansi.esc(ansi.FG_BLUE))
    border_top = attr.ib(default = "─")
    border_right = attr.ib(default=" │ ")
    border_bottom = attr.ib(default = "─")
    border_left = attr.ib(default="│ ")
    corners = attr.ib(default=('┌','┐','└','┘',))
    align = attr.ib(default='<')
    reset = attr.ib(default=ansi.esc(ansi.RESET_ALL))

    _row_format = None

    def cell(self, x, text):
        values = attr.asdict(self)
        values['text'] = text

        s = "{text_style}{text}{reset}{border_style}{border_right}"
        if x == 0:
            s = "{border_style}{border_left}" + s
        return s.format(**values)

    def render(self, cols, pads):
        n = 0
        if self._row_format is None:
            row_format = ''
            for pad in pads:
                row_format += self.cell(n, "{:" + self.align + str(pad) + "}")
                n += 1
            self._row_format = row_format
        return self._row_format.format(*cols)

@attr.s
class Row(list):
    style = attr.ib(default=attr.Factory(RowStyle))
    items = attr.ib(default=attr.Factory(list))

    def render(self, col_widths):
        return self.style.render(self.items, col_widths)

class AsciiTable(object):
    cell = RowStyle()
    head = RowStyle(align='^')

    head.text_style=ansi.esc(ansi.UNDERLINE, ansi.FG_BLUE, ansi.BRIGHT)

    def __init__(self, col_widths=[0]):
        self.rows = []
        self.col_width = col_widths

    def header_row(self, vals):
        vals = ["*%s*" % val for val in vals]
        return self.row(vals, self.head)

    def row(self, vals, style=None):
        if style is None:
            style = self.cell

        col=0
        if len(vals) == 1:
            vals = vals.pop()

        items = []
        for val in vals:
            if col >= len(self.col_width):
                self.col_width.append(0)
            val = val.strip()
            if len(val) > self.col_width[col]:
                self.col_width[col] = len(val)
            elif self.col_width[col] == 0:
                self.col_width[col] = 1
            items.append(val)
            col += 1
        row = Row(style=style, items=items)
        self.rows.append(row)

    def render(self):
        rows = []
        for row in self.rows:
            row = row.render(self.col_width)
            rows.append(row)

        table_width = sum(self.col_width) + (3 * len(self.rows[0].items)) + 1
        cell = self.cell
        line = cell.border_bottom * (table_width-2)
        head = self.head.border_style + cell.corners[0] + line + cell.corners[1]
        foot = cell.corners[2] + line + cell.corners[3]

        rows = [head] + rows + [foot]
        return "\n".join(rows)

    def __repr__(self):
        return self.render()
