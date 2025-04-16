"""
Export list of drives (or a drive's details if `drive_id` argument is given).
"""
import logging
import os
from argparse import ArgumentParser
from urllib.parse import quote_plus

import requests
from zut import TabularDumper, format_csv_value, tabular_dumper, dump_object

from . import M365Client, settings

_logger = logging.getLogger(__name__)


def add_arguments(parser: ArgumentParser):
    parser.add_argument('drive_id', nargs='?', help="export details of this drive only")
    parser.add_argument('-o', '--out', help="output file (CSV, or JSON if `drive_id` argument is given)")


def handle(m365: M365Client, drive_id: str|None = None, *, out: str|os.PathLike|None = None):
    if drive_id:
        if not isinstance(drive_id, str):
            raise TypeError(f"Invalid type for argument 'drive_id': {type(drive_id).__name__}")
        
        if out == '.':
            out = '{title}.json'

        data = m365.get(f'/drives/{quote_plus(drive_id)}')
        dump_object(data, out, title=f"drive_{data['id']}" if out else None, dir=settings.DATA_DIR)

    else:
        if not out:
            out = '{title}.csv'
        
        with tabular_dumper(out, title="drive", dir=settings.DATA_DIR) as dumper:
            _logger.info("Get site drives")
            for data in m365.iter('/sites?$select=id,displayName'):
                endpoint = f"/sites/{data['id']}/drives"
                _handle_by_type(m365, dumper, endpoint, 'site', data['id'], data.get('displayName'))

            _logger.info("Get user drives")
            for data in m365.iter('/users?$select=id,displayName'):
                endpoint = f"/users/{data['id']}/drives"
                _handle_by_type(m365, dumper, endpoint, 'user', data['id'], data.get('displayName'))

            _logger.info("Get group drives")
            for data in m365.iter('/groups?$select=id,displayName'):
                endpoint = f"/groups/{data['id']}/drives"
                _handle_by_type(m365, dumper, endpoint, 'group', data['id'], data.get('displayName'))


def _handle_by_type(m365: M365Client, dumper: TabularDumper, endpoint: str, parent_type, parent_id, parent_displayName):
    def get_user_info(data: dict):
        if user := data.get('user'):
            if email := user.get('email'):
                return email
            elif displayName := user.get('displayName'):
                return displayName
            elif id := user.get('id'):
                return id
            else:
                return format_csv_value(user, visual=True)
        elif group := data.get('group'):
            return f"group:{group['id']} ({group['displayName']})"
        else:
            return format_csv_value(user, visual=True)

    try:
        for data in m365.iter(endpoint):
            dumper.dump({
                'id': data['id'],
                'webUrl': data['webUrl'],
                'name': data['name'],
                'description': data['description'],
                'driveType': data['driveType'],
                'owner': get_user_info(data['owner']),
                'createdBy': get_user_info(data['createdBy']),
                'createdDateTime': data['createdDateTime'],
                'lastModifiedDateTime': data['lastModifiedDateTime'],
                'quota_state': data['quota']['state'],
                'quota_total': data['quota']['total'] / 1024**3,
                'quota_used': data['quota']['used'] / 1024**3,
                'quota_deleted': data['quota']['deleted'] / 1024**3,
                'quota_remaining': data['quota']['remaining'] / 1024**3,
                'parent_type': parent_type,
                'parent_id': parent_id,
                'parent_displayName': parent_displayName,
            })
    except requests.HTTPError as err:
        if err.response.status_code == 404:
            pass # parent has no drives
        else:
            raise
