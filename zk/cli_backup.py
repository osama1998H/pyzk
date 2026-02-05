# -*- coding: utf-8 -*-
import argparse
import sys

from . import ZK
from .backup import erase_device, export_backup, load_backup, restore_backup, save_backup
from .exception import ZKErrorResponse, ZKNetworkError


class BasicException(Exception):
    pass


def _print(msg):
    try:
        sys.stdout.write(msg + '\n')
    except Exception:
        pass


def main(argv=None):
    parser = argparse.ArgumentParser(description='ZK Backup/Restore Tool')
    parser.add_argument('-a', '--address',
                        help='ZK device Address [192.168.1.201]', default='192.168.1.201')
    parser.add_argument('-p', '--port', type=int,
                        help='ZK device port [4370]', default=4370)
    parser.add_argument('-T', '--timeout', type=int,
                        help='Default [10] seconds (0: disable timeout)', default=10)
    parser.add_argument('-P', '--password', type=int,
                        help='Device code/password', default=0)
    parser.add_argument('-f', '--force-udp', action='store_true',
                        help='Force UDP communication')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print debug information')
    parser.add_argument('-E', '--erase', action='store_true',
                        help='Clean the device after writing backup')
    parser.add_argument('-r', '--restore', action='store_true',
                        help='Restore from backup')
    parser.add_argument('-c', '--clear-attendance', action='store_true',
                        help='On restore, also clears the attendance [default keep attendance]')
    parser.add_argument('-g', '--high-rate', action='store_true',
                        help='In restoration, use high-rate mode')
    parser.add_argument('filename', nargs='?',
                        help='backup filename (default [serialnumber].json.bak)', default='')

    args = parser.parse_args(argv)

    zk = ZK(args.address, port=args.port, timeout=args.timeout, password=args.password,
            force_udp=args.force_udp, verbose=args.verbose)
    conn = None
    try:
        _print('Connecting to device ...')
        conn = zk.connect()
        serialnumber = conn.get_serialnumber()
        fp_version = conn.get_fp_version()
        _print('Serial Number    : {}'.format(serialnumber))
        _print('Finger Version   : {}'.format(fp_version))
        filename = args.filename if args.filename else '{}.json.bak'.format(serialnumber)
        _print('')

        if not args.restore:
            _print('--- sizes & capacity ---')
            conn.read_sizes()
            _print(str(conn))
            _print('--- Export Users & Templates ---')
            data = export_backup(conn)
            save_backup(conn, filename, data=data)
            _print('Saved to file {}'.format(filename))
            if args.erase:
                erase_device(conn, clear_attendance=args.clear_attendance, prompt_serial=True)
                _print('Device erased after backup')
        else:
            _print('Reading file {}'.format(filename))
            data = load_backup(filename)
            _print('Restoring Data...')
            restore_backup(conn, data, erase=True, clear_attendance=args.clear_attendance,
                           high_rate=args.high_rate, prompt_serial=True)
            conn.read_sizes()
            _print('--- final sizes & capacity ---')
            _print(str(conn))
    except BasicException as e:
        _print(str(e))
    except (ZKErrorResponse, ZKNetworkError) as e:
        _print('Error: {}'.format(e))
    except Exception as e:
        _print('Process terminate : {}'.format(e))
        _print('Error: {}'.format(sys.exc_info()[0]))
    finally:
        if conn:
            try:
                _print('Enabling device ...')
                conn.enable_device()
            except Exception:
                pass
            try:
                conn.disconnect()
            except Exception:
                pass
            _print('ok bye!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
