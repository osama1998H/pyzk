.. toctree::
   :caption: Attendance Log Operation
   :name: topic3

########################
Attendance Log Operation
########################

Get attendance log
------------------

.. code-block:: python

    records = conn.get_attendance()
    for record in records:
        print(record.user_id, record.timestamp, record.status, record.punch)

Attendance fields
-----------------

Each record is an ``Attendance`` object with:

- ``user_id``: external user identifier
- ``timestamp``: ``datetime`` when the punch happened
- ``status``: event status code (device specific)
- ``punch``: punch type (device specific)

Clear attendance log
--------------------

.. code-block:: python

    conn.clear_attendance()

Live capture
------------

Live capture emits attendance events in near real time.

.. code-block:: python

    for event in conn.live_capture():
        if event is None:
            continue
        print(event)
