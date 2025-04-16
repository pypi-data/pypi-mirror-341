"""
Export list of groups (or a group's details if `group_id` argument is given).
"""
import os
from argparse import ArgumentParser
from urllib.parse import quote_plus
from uuid import UUID

from zut import dump_object, tabular_dumper

from . import M365Client, settings


def add_arguments(parser: ArgumentParser):
    parser.add_argument('group_id', nargs='?', help="export details of this group ID only")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `group_id` argument is given)")
    

def handle(m365: M365Client, group_id: str|UUID|None = None, *, out: str|os.PathLike|None = None):
    if group_id:
        if isinstance(group_id, UUID):
            group_id = str(group_id)
        elif not isinstance(group_id, str):
            raise TypeError(f"Invalid type for argument 'group_id': {type(group_id).__name__}")
        
        if out == '.':
            out = '{title}.json'

        data = m365.get(f'/groups/{quote_plus(group_id)}')
        dump_object(data, out, title=f"group_{data['id']}" if out else None, dir=settings.DATA_DIR)
    
    else:
        if not out:
            out = '{title}.csv'

        export_group_list(m365, out=out)


def export_group_list(m365: M365Client, *, out='{title}.csv', title='group'):
    with tabular_dumper(out, headers=["id", "displayName", "*"], delay=True, title=title, dir=settings.DATA_DIR) as dumper:
        for data in m365.iter('/groups'):
            dumper.dump(data)
