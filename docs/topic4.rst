.. toctree::
   :caption: Device maintenance
   :name: topic4

##################
Device Maintenance
##################

Set time
--------

.. code-block:: python

    from datetime import datetime
    conn.set_time(datetime.today())

Poweroff
--------

.. code-block:: python

    conn.poweroff()

Restart
-------

.. code-block:: python

    conn.restart()

Clear buffer
------------

``free_data()`` clears the internal device buffer used for bulk reads.

.. code-block:: python

    conn.free_data()

Clear data
----------

**Warning:** this erases users, fingerprints, and logs.

.. code-block:: python

    conn.clear_data()

Unlock door
-----------

On supported devices, ``unlock`` triggers the door relay for a few seconds.

.. code-block:: python

    conn.unlock(time=3)
