# -*- coding: utf-8 -*-
import unittest

from zk.backup import BACKUP_VERSION, restore_backup
from zk.exception import ZKErrorResponse
from zk.finger import Finger
from zk.user import User


class FakeConn(object):
    def __init__(self, fp_version='10', serial='ABC'):
        self._fp_version = fp_version
        self._serial = serial
        self.saved = []
        self.hr_saved = []
        self.disabled = False
        self.enabled = False
        self.cleared = False
        self.att_cleared = False

    def get_fp_version(self):
        return self._fp_version

    def get_serialnumber(self):
        return self._serial

    def disable_device(self):
        self.disabled = True

    def clear_data(self):
        self.cleared = True

    def clear_attendance(self):
        self.att_cleared = True

    def enable_device(self):
        self.enabled = True

    def save_user_template(self, user, temps):
        self.saved.append((user, temps))

    def HR_save_usertemplates(self, usertemplates):
        self.hr_saved = usertemplates


class FingerJsonRoundTripTest(unittest.TestCase):
    def test_roundtrip(self):
        template = b'\x01\x02\x03\x04\x05\x06\x07\x08'
        finger = Finger(1, 2, 1, template)
        data = finger.json_pack()
        decoded = Finger.json_unpack(data)
        self.assertEqual(finger.uid, decoded.uid)
        self.assertEqual(finger.fid, decoded.fid)
        self.assertEqual(finger.valid, decoded.valid)
        self.assertEqual(finger.template, decoded.template)


class BackupRestoreTest(unittest.TestCase):
    def _sample_data(self):
        user = User(1, 'Alice', 0, '', '', '1', 0)
        finger = Finger(1, 0, 1, b'\x01\x02')
        return {
            'version': BACKUP_VERSION,
            'serial': 'ABC',
            'fp_version': '10',
            'users': [user.__dict__],
            'templates': [finger.json_pack()],
        }

    def test_restore_calls_save_user_template(self):
        conn = FakeConn(fp_version='10', serial='ABC')
        data = self._sample_data()
        restore_backup(conn, data, erase=False, high_rate=False, prompt_serial=False)
        self.assertEqual(len(conn.saved), 1)
        self.assertEqual(len(conn.hr_saved), 0)
        self.assertTrue(conn.enabled)

    def test_restore_high_rate(self):
        conn = FakeConn(fp_version='10', serial='ABC')
        data = self._sample_data()
        restore_backup(conn, data, erase=False, high_rate=True, prompt_serial=False)
        self.assertEqual(len(conn.saved), 0)
        self.assertEqual(len(conn.hr_saved), 1)

    def test_fp_version_mismatch(self):
        conn = FakeConn(fp_version='9', serial='ABC')
        data = self._sample_data()
        with self.assertRaises(ZKErrorResponse):
            restore_backup(conn, data, erase=False, high_rate=False, prompt_serial=False)


if __name__ == '__main__':
    unittest.main()
