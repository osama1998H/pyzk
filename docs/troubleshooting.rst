.. toctree::
   :caption: Troubleshooting
   :name: troubleshooting

###############
Troubleshooting
###############

Device not reachable
--------------------

- Verify IP and port (default 4370).
- Ensure the device is on the same network/VLAN.
- Try ``force_udp=True`` if TCP times out.

Ping fails
----------

Some networks block ICMP. Set ``ommit_ping=True`` to skip ping checks.

Garbled names
-------------

Set ``encoding`` to match your device language, for example ``'gbk'``.

Slow template reads
-------------------

Template downloads can be large. Increase ``timeout`` and avoid Wi-Fi if possible.

Restore fails with template version mismatch
-------------------------------------------

Fingerprint template formats vary. Restore only to devices with the same
``fp_version``.
