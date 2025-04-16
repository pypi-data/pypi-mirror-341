"""
Export list of calendars (or a calendar's details if `calendar_id` argument is given).

See:
- API endpoints:
    - https://learn.microsoft.com/en-us/graph/api/user-list-calendargroups?view=graph-rest-1.0&tabs=http
    - https://learn.microsoft.com/en-us/graph/api/user-list-calendars?view=graph-rest-1.0&tabs=http
- Event type: https://learn.microsoft.com/en-us/graph/api/resources/event?view=graph-rest-1.0

Note: it is not possible to extract group calendar or group calendar events from an application (only delegated permissions are supported - which would require being a member of each group).
See https://learn.microsoft.com/en-us/graph/api/calendar-list-events?view=graph-rest-beta&tabs=http#permissions
"""
from datetime import timedelta
import logging
import os
from argparse import ArgumentParser
from time import time_ns
from urllib.parse import quote_plus
from uuid import UUID

from zut import dump_object, files, is_tabular_path, tabular_dumper

from . import M365Client, settings

_logger = logging.getLogger(__name__)


def add_arguments(parser: ArgumentParser):
    parser.add_argument('user', nargs='?', help="export list of calendar events for this user only (or FROM this user with `--from-user` option), given as its ID or userPrincipalName (usually the email)")
    parser.add_argument('--from-user', action='store_true', help="export list of calendar events for all users starting from the given `user` argument")
    parser.add_argument('-o', '--out', default='{title}.csv', help="output file (CSV)")
    

def handle(m365: M365Client, user: str|UUID|None = None, *, from_user = False, out: str|os.PathLike = '{title}.csv'):
    if from_user:
        if not user:
            raise ValueError("Argument 'user' is required for option 'from_user'")

    if user and not from_user:
        export_user_calendar_list(m365, user, out=out)
    else:
        export_calendar_list(m365, from_user=from_user, out=out)


def export_calendar_list(m365: M365Client, *, from_user: str|UUID|None = None, out='{title}.csv'):
    if isinstance(from_user, UUID):
        from_user = str(from_user)
    
    if from_user:
        started = False
        title = f'calendar-from-{from_user}'
    else:
        title = f'calendar'

    out = files.in_dir(out, dir=settings.DATA_DIR, title=title)
    files.remove(out, missing_ok=True)
    
    t0 = time_ns()
    _logger.info(f"Dump calendars to {out} …")
    total_count = 0

    for user_data in m365.iter('/users'):
        if from_user and not started:
            if user_data['userPrincipalName'] == from_user or user_data['id'] == from_user:
                started = True
            else:
                continue

        try:
            _logger.info("Search calendars for user %s …", user_data['userPrincipalName'])
            count = export_user_calendar_list(m365, user_data, out=out, title=None, append=True)
            total_count += count
            _logger.info("%s calendars found for user %s", count, user_data['userPrincipalName'])
        except Exception as err:
            _logger.exception("Error while exporting calendars for user %s" % (user_data['userPrincipalName'],))

    _logger.info(f"{total_count:,} calendars exported to {out} in {timedelta(seconds=int((time_ns() - t0)/1E9))}")


def export_user_calendar_list(m365: M365Client, user: str|UUID|dict, *, out='{title}.csv', title='calendar-{user}', append=False):
    if isinstance(user, str):
        try:
            user = UUID(user)
        except ValueError:
            pass # user is not a uuid
    
    owner_id = None
    user_principal_name = None
    if isinstance(user, UUID):
        owner_id = user
    elif isinstance(user, str):
        user_principal_name = user
    elif isinstance(user, dict):
        owner_id = user['id']
        user_principal_name = user['userPrincipalName']
    else:
        raise TypeError(f"Invalid type for argument 'user': {type(user).__name__}")
    
    if isinstance(title, str):
        title = title.format(user=user_principal_name or owner_id)

    endpoint = f'/users/{owner_id or quote_plus(user_principal_name)}/calendars'
    if not is_tabular_path(out):
        if out == '.':
            out = '{title}.json'

        data_list = m365.get(endpoint)
        dump_object(data_list, out, title=title, dir=settings.DATA_DIR)
        return len(data_list)
    else:
        with tabular_dumper(out, headers=['id', 'ownerId', 'userPrincipalName', 'name', 'isDefaultCalendar', 'canEdit'], title=title, append=append, dir=settings.DATA_DIR) as dumper:
            try:
                for data in m365.iter(endpoint):
                    dumper.dump({
                        'id': data['id'],
                        'ownerId': owner_id,
                        'userPrincipalName': user_principal_name,
                        'name': data['name'],
                        'isDefaultCalendar': data['isDefaultCalendar'],
                        'canEdit': data['canEdit'],
                    })
            except m365.MailboxInactiveError:
                _logger.debug("Mailbox inactive for user %s", owner_id or user_principal_name)
                return 0

        return dumper.count
