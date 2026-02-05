# -*- coding: utf-8 -*-
import io
import json
import sys

from .exception import ZKErrorResponse
from .user import User
from .finger import Finger

BACKUP_VERSION = '1.00jut'


def _write_line(msg):
    try:
        sys.stdout.write(msg + '\n')
    except Exception:
        pass


def _prompt_input(prompt):
    try:
        return input(prompt)
    except NameError:
        return raw_input(prompt)


def _validate_data(data):
    required = ['version', 'serial', 'fp_version', 'users', 'templates']
    for key in required:
        if key not in data:
            raise ZKErrorResponse('Backup file missing key: {}'.format(key))
    if data['version'] != BACKUP_VERSION:
        raise ZKErrorResponse('Unsupported backup version: {}'.format(data['version']))
    return True


def export_backup(conn):
    """
    Export users and templates from a connected device.

    :param conn: ZK connection
    :return: dict ready to be JSON serialized
    """
    serial = conn.get_serialnumber()
    fp_version = conn.get_fp_version()
    conn.read_sizes()
    users = conn.get_users()
    if len(users) == 0:
        raise ZKErrorResponse('Empty user list, aborting backup')
    templates = conn.get_templates()
    return {
        'version': BACKUP_VERSION,
        'serial': serial,
        'fp_version': fp_version,
        'users': [u.__dict__ for u in users],
        'templates': [t.json_pack() for t in templates]
    }


def save_backup(conn, path, data=None):
    if data is None:
        data = export_backup(conn)
    with io.open(path, 'w', encoding='utf-8') as output:
        json.dump(data, output, indent=1)
    return path


def load_backup(path):
    with io.open(path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    _validate_data(data)
    return data


def _confirm_serial(expected_serial):
    _write_line('WARNING! the next step will erase the current device content.')
    _write_line('Please input the serial number of this device [{}] to acknowledge the ERASING!'.format(expected_serial))
    new_serial = _prompt_input('Serial Number    : ')
    return new_serial == expected_serial


def erase_device(conn, clear_attendance=False, prompt_serial=True):
    serial = conn.get_serialnumber()
    if prompt_serial and not _confirm_serial(serial):
        raise ZKErrorResponse('Serial number mismatch')
    conn.disable_device()
    conn.clear_data()
    if clear_attendance:
        conn.clear_attendance()
    return True


def restore_backup(conn, data, erase=False, clear_attendance=False, high_rate=False, prompt_serial=True):
    """
    Restore users and templates to a connected device.

    :param conn: ZK connection
    :param data: dict from load_backup/export_backup
    :param erase: clear device before restore
    :param clear_attendance: clear attendance log while erasing
    :param high_rate: use high-rate bulk write
    :param prompt_serial: confirm serial number before erasing
    """
    _validate_data(data)
    fp_version = conn.get_fp_version()
    if data['fp_version'] != fp_version:
        raise ZKErrorResponse('Fingerprint version mismatch {} != {}'.format(fp_version, data['fp_version']))

    if erase:
        erase_device(conn, clear_attendance=clear_attendance, prompt_serial=prompt_serial)

    users = [User.json_unpack(u) for u in data['users']]
    templates = [Finger.json_unpack(t) for t in data['templates']]

    by_uid = {}
    for t in templates:
        by_uid.setdefault(t.uid, []).append(t)

    if high_rate:
        usertemplates = []
        for u in users:
            usertemplates.append([u, by_uid.get(u.uid, [])])
        conn.HR_save_usertemplates(usertemplates)
    else:
        for u in users:
            conn.save_user_template(u, by_uid.get(u.uid, []))

    conn.enable_device()
    return True
