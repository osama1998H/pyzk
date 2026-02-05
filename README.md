# pyzk

[![Build Status](https://travis-ci.org/fananimi/pyzk.svg?branch=master)](https://travis-ci.org/fananimi/pyzk)

`pyzk` is an unofficial library of zksoftware (zkteco family) attendance machine.

# Installation

There is some installation method you can use below:

* pip
```sh
pip install -U pyzk
```

* manual installation (clone and execute)

```sh
python setup.py install
```

* clone and append the path of this project

```python
import sys
import os
sys.path.insert(1,os.path.abspath("./pyzk"))
from zk import ZK, const
```

# Documentation

Complete documentation can be found at [Readthedocs](http://pyzk.readthedocs.io/en/latest/ "pyzk's readthedocs") .

# API Usage

Create the ZK object and you will be ready to call api.

## Basic Usage

The following is an example code block how to use pyzk.

```python
from zk import ZK, const

conn = None
# create ZK instance
zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    users = conn.get_users()
    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        print ('+ UID #{}'.format(user.uid))
        print ('  Name       : {}'.format(user.name))
        print ('  Privilege  : {}'.format(privilege))
        print ('  Password   : {}'.format(user.password))
        print ('  Group ID   : {}'.format(user.group_id))
        print ('  User  ID   : {}'.format(user.user_id))

    # Test Voice: Say Thank You
    conn.test_voice()
    # re-enable device after all commands already executed
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
```

## Command List

* Connect/Disconnect

```python
conn = zk.connect()
conn.disconnect()
```

* Disable/Enable Connected Device

```python
# disable (lock) device, to ensure no user activity in device while some process run
conn.disable_device()
# re-enable the connected device and allow user activity in device again
conn.enable_device()
```

* Get and Set Time

```python
from datetime import datetime
# get current machine's time
zktime = conn.get_time()
print zktime
# update new time to machine
newtime = datetime.today()
conn.set_time(newtime)
```


* Ger Firmware Version and Extra Information

```python
conn.get_firmware_version()
conn.get_serialnumber()
conn.get_platform()
conn.get_device_name()
conn.get_face_version()
conn.get_fp_version()
conn.get_extend_fmt()
conn.get_user_extend_fmt()
conn.get_face_fun_on()
conn.get_compat_old_firmware()
conn.get_network_params()
conn.get_mac()
conn.get_pin_width()
```

* Get Device Usage Space

```python
conn.read_sizes()
print(conn)
#also:
conn.users
conn.fingers
conn.records
conn.users_cap
conn.fingers_cap
# TODO: add records_cap counter
# conn.records_cap
```

* User Operation

```python
# Create user
conn.set_user(uid=1, name='Fanani M. Ihsan', privilege=const.USER_ADMIN, password='12345678', group_id='', user_id='123', card=0)
# Get all users (will return list of User object)
users = conn.get_users()
# Delete User
conn.delete_user(uid=1)
conn.delete_user(user_id=123)
```

* Fingerprints

```python
# Get  a single Fingerprint (will return a Finger object)
template = conn.get_user_template(uid=1, temp_id=0) #temp_id is the finger to read 0~9
# Get all fingers from DB (will return a list of Finger objects)
fingers = conn.get_templates()

# to restore a finger, we need to assemble with the corresponding user
# pass a User object and a list of finger (max 10) to save
conn.save_user_template(user, [fing1 ,fing2])
```

* High rate transfer

you can use the high rate mode to fasten the uploading of users and finger templates, you just need actual instances of users and fingers in a corresponding list/array.

```python
usertemplates = [
    [user_1, [user_finger_1, user_finger_2]],
    [user_2, [finger_3]],
    ...
]
conn.HR_save_usertemplates(usertemplates)
```




* Remote Fingerprint Enrollment
```python
zk.enroll_user('1')
# but it doesn't work with some tcp ZK8 devices
```


* Attendance Record
```python
# Get attendances (will return list of Attendance object)
attendances = conn.get_attendance()
# Clear attendances records
conn.clear_attendance()
```

* Test voice

```python
"""
 play test voice:
  0 Thank You
  1 Incorrect Password
  2 Access Denied
  3 Invalid ID
  4 Please try again
  5 Dupicate ID
  6 The clock is flow
  7 The clock is full
  8 Duplicate finger
  9 Duplicated punch
  10 Beep kuko
  11 Beep siren
  12 -
  13 Beep bell
  14 -
  15 -
  16 -
  17 -
  18 Windows(R) opening sound
  19 -
  20 Fingerprint not emolt
  21 Password not emolt
  22 Badges not emolt
  23 Face not emolt
  24 Beep standard
  25 -
  26 -
  27 -
  28 -
  29 -
  30 Invalid user
  31 Invalid time period
  32 Invalid combination
  33 Illegal Access
  34 Disk space full
  35 Duplicate fingerprint
  36 Fingerprint not registered
  37 -
  38 -
  39 -
  40 -
  41 -
  42 -
  43 -
  43 -
  45 -
  46 -
  47 -
  48 -
  49 -
  50 -
  51 Focus eyes on the green box
  52 -
  53 -
  54 -
  55 -
"""
conn.test_voice(index=0) # will say 'Thank You'
```

* Device Maintenance

```python
# DANGER!!! This command will be erase all data in the device (incuded: user, attendance report, and finger database)
conn.clear_data()
# shutdown connected device
conn.poweroff()
# restart connected device
conn.restart()
# clear buffer
conn.free_data()
```

* Live Capture!

```python
# live capture! (timeout at 10s)
for attendance in conn.live_capture():
    if attendance is None:
        # implement here timeout logic
        pass
    else:
        print (attendance) # Attendance object

    #if you need to break gracefully just set
    #   conn.end_live_capture = True
    #
    # On interactive mode,
    # use Ctrl+C to break gracefully
    # this way it restores timeout
    # and disables live capture
```

**Test Machine**

```sh
usage: ./test_machine.py [-h] [-a ADDRESS] [-p PORT] [-T TIMEOUT] [-P PASSWORD]
                         [-f] [-t] [-r] [-u] [-l] [-D DELETEUSER] [-A ADDUSER]
                         [-E ENROLLUSER] [-F FINGER]

ZK Basic Reading Tests

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        ZK device Address [192.168.1.201]
  -p PORT, --port PORT  ZK device port [4370]
  -T TIMEOUT, --timeout TIMEOUT
                        Default [10] seconds (0: disable timeout)
  -P PASSWORD, --password PASSWORD
                        Device code/password
  -b, --basic           get Basic Information only. (no bulk read, ie: users)
  -f, --force-udp       Force UDP communication
  -v, --verbose         Print debug information
  -t, --templates       Get templates / fingers (compare bulk and single read)
  -tr, --templates-raw  Get raw templates (dump templates)
  -r, --records         Get attendance records
  -u, --updatetime      Update Date/Time
  -l, --live-capture    Live Event Capture
  -o, --open-door       Open door

  -D DELETEUSER, --deleteuser DELETEUSER
                        Delete a User (uid)
  -A ADDUSER, --adduser ADDUSER
                        Add a User (uid) (and enroll)
  -E ENROLLUSER, --enrolluser ENROLLUSER
                        Enroll a User (uid)
  -F FINGER, --finger FINGER
                        Finger for enroll (fid=0)

```

**Backup/Restore (Users and fingers only!!!)** *(WARNING! destructive test! do it at your own risk!)*

Use the installed CLI:

```sh
pyzk-backup --help
pyzk-backup -a 192.168.1.201
pyzk-backup -a 192.168.1.201 --restore backup.json.bak
```

The legacy script `test_backup_restore.py` now wraps the same CLI and accepts
the same flags.

To restore on a different device, make sure to specify the `filename`. on restoring, it asks for the serial number of the destination device (to make sure it was correct, as it deletes all data) WARNING. there is no way to restore attendance data, you can keep it or clear it, but once cleared, there is no way to restore it.

# Compatible devices

See `docs/compatible_devices.rst` for the canonical list and the submission template.

# Roadmap

- Create better documentation (in progress)
- Finger template downloader & uploader (in progress, via `pyzk-backup`)
- HTTP REST API (spec only)
- Real-time API (spec only)
- Expand compatible devices list and contribution guide (in progress)
- Future ideas are tracked in `ROADMAP.md`
