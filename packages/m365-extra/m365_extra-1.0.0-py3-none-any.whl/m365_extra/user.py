"""
Export list of users (or a user's details if `user` argument is given).
"""
import os
from argparse import ArgumentParser
from urllib.parse import quote_plus
from uuid import UUID

from zut import dump_object, tabular_dumper

from . import M365Client, settings


def add_arguments(parser: ArgumentParser):
    parser.add_argument('user', nargs='?', help="export details of this user only, given as its ID or userPrincipalName (usually the email)")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `user` argument is given)")
    

def handle(m365: M365Client, user: str|UUID|None = None, *, out: str|os.PathLike|None = None):
    if user:
        if isinstance(user, UUID):
            user = str(user)
        elif not isinstance(user, str):
            raise TypeError(f"Invalid type for argument 'user': {type(user).__name__}")
        
        if out == '.':
            out = '{title}.json'

        data = m365.get(f'/users/{quote_plus(user)}')
        dump_object(data, out, title=f"user_{data['userPrincipalName']}" if out else None, dir=settings.DATA_DIR)
    
    else:
        if not out:
            out = '{title}.csv'
        
        export_user_list(m365, out=out)


def export_user_list(m365: M365Client, *, out='{title}.csv', title='user'):
    with tabular_dumper(out, headers=["id", "userPrincipalName", "displayName", "givenName", "surname", "mail", "businessPhones", "mobilePhone", "jobTitle", "officeLocation", "preferredLanguage"], delay=True, title=title, dir=settings.DATA_DIR) as dumper:
        for data in m365.iter('/users'):
            dumper.dump(data)
