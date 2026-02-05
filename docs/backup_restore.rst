.. toctree::
   :caption: Backup & Restore
   :name: backup_restore

################
Backup & Restore
################

pyzk includes a supported CLI and helper functions to export and restore users
and fingerprint templates.

CLI usage
---------

The ``pyzk-backup`` command mirrors the legacy ``test_backup_restore.py`` script
but is installed as a console entry point.

.. code-block:: sh

    pyzk-backup -a 192.168.1.201
    pyzk-backup -a 192.168.1.201 --restore backup.json.bak

Options
-------

- ``-E / --erase``: erase the device after writing the backup file
- ``-r / --restore``: restore from backup file
- ``-c / --clear-attendance``: also clears attendance when restoring
- ``-g / --high-rate``: use high-rate bulk write

Programmatic usage
------------------

.. code-block:: python

    from zk import ZK
    from zk.backup import export_backup, save_backup, load_backup, restore_backup

    conn = ZK('192.168.1.201').connect()

    data = export_backup(conn)
    save_backup(conn, 'device.json.bak', data=data)

    data = load_backup('device.json.bak')
    restore_backup(conn, data, erase=True, prompt_serial=True)

JSON schema
-----------

The backup file is a JSON document with these fields:

- ``version``: backup schema version (currently ``1.00jut``)
- ``serial``: device serial number
- ``fp_version``: fingerprint template version
- ``users``: list of user objects
- ``templates``: list of fingerprint templates

Notes
-----

- Restoring always requires a matching fingerprint template version.
- For safety, the CLI prompts for the device serial number before erasing.
