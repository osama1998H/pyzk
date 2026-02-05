.. toctree::
   :caption: Connect / Disconnect to Machine
   :name: topic1

###############################
Connect / Disconnect to Machine
###############################

Create a client
---------------

The main entry point is the ``ZK`` class from ``zk.base``. It encapsulates
socket creation, handshake, and command framing.

.. code-block:: python

    from zk import ZK

    zk = ZK(
        '192.168.1.201',
        port=4370,
        timeout=10,
        password=0,
        force_udp=False,
        ommit_ping=False,
        verbose=False,
        encoding='UTF-8',
    )

Connect
-------

.. code-block:: python

    conn = zk.connect()
    conn.disable_device()  # recommended for bulk reads/writes

Disconnect
----------

.. code-block:: python

    conn.enable_device()
    conn.disconnect()

TCP vs UDP
----------

By default, pyzk uses TCP. Some devices and firmware revisions are more stable
with UDP; use ``force_udp=True`` when you see intermittent timeouts.

Ping behavior
-------------

If ``ommit_ping=False``, the library may attempt to ping the device before
connecting. Set it to ``True`` if ICMP is blocked in your network.

Encoding
--------

If names appear garbled, pass the correct device encoding (for example ``'gbk'``
for some iFace devices).
