.. toctree::
   :caption: IOT
   :name: topic5

###
IOT
###

You can build simple IOT workflows using pyzk and a small controller such as a
Raspberry Pi. A common example is triggering a door relay from attendance events.

Door Lock Open
--------------

This example listens to live capture events and unlocks the door when a known
user punches in.

.. code-block:: python

    from zk import ZK

    zk = ZK('192.168.1.201')
    conn = zk.connect()
    conn.disable_device()

    allowed = set(['1001', '1002'])

    for event in conn.live_capture():
        if event is None:
            continue
        if event.user_id in allowed:
            conn.unlock(time=3)

    conn.enable_device()
    conn.disconnect()

**Warning:** the ``unlock`` operation can trigger real hardware. Use caution and
test on a controlled system first.
