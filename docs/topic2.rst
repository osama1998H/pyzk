.. toctree::
   :caption: User Operation
   :name: topic2

##############
User Operation
##############

Create or update a user
-----------------------

.. code-block:: python

    from zk import ZK, const

    conn = ZK('192.168.1.201').connect()
    conn.disable_device()
    conn.set_user(
        uid=1,
        name='Alice',
        privilege=const.USER_ADMIN,
        password='1234',
        group_id='',
        user_id='1',
        card=0,
    )
    conn.enable_device()
    conn.disconnect()

Get users
---------

.. code-block:: python

    users = conn.get_users()
    for user in users:
        print(user.uid, user.user_id, user.name)

Delete a user
-------------

.. code-block:: python

    conn.delete_user(uid=1)
    # or
    conn.delete_user(user_id='1')

Enroll user (remote)
--------------------

This triggers enrollment on the device. It may not work on some TCP devices.

.. code-block:: python

    conn.enroll_user(uid=1, temp_id=0)

Privileges
----------

``const.USER_DEFAULT`` and ``const.USER_ADMIN`` are the most common privileges.
Some devices use additional values; check ``zk/const.py`` for the full list.

UID vs User ID
--------------

``uid`` is the internal device ID. ``user_id`` is your external identifier.
Some older devices expect them to match. If unsure, set ``user_id`` to
``str(uid)``.
