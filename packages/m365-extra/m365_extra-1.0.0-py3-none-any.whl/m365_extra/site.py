"""
Export list of sites (or a site's details if `site_id` argument is given).
"""
import os
from argparse import ArgumentParser
from urllib.parse import quote_plus

from zut import tabular_dumper, dump_object

from . import M365Client, settings


def add_arguments(parser: ArgumentParser):
    parser.add_argument('site_id', nargs='?', help="export details of this site only")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `site_id` argument is given)")
    

def handle(m365: M365Client, site_id: str|None = None, *, out: str|os.PathLike|None = None):
    if site_id:
        if not isinstance(site_id, str):
            raise TypeError(f"Invalid type for argument 'site_id': {type(site_id).__name__}")
        
        if out == '.':
            out = '{title}.json'

        data = m365.get(f'/sites/{quote_plus(site_id)}')
        dump_object(data, out, title=f"site_{data['id']}" if out else None, dir=settings.DATA_DIR)

    else:
        if not out:
            out = '{title}.csv'

        with tabular_dumper(out, headers=['id', 'webUrl', 'displayName', '*'], optional=['name', 'displayName'], title='site', dir=settings.DATA_DIR) as dumper:
            for user in m365.iter('/sites'):
                dumper.dump(user)
