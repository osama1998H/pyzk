.. toctree::
   :caption: HTTP & Real-Time API (Spec)
   :name: api_design

###############################
HTTP & Real-Time API (Spec Only)
###############################

This is a forward-looking design spec for a REST and real-time API built on top
of pyzk. It does **not** include an implementation yet.

Goals
-----

- Provide a simple HTTP interface for device operations and data extraction.
- Support real-time events via server-sent events (SSE).
- Keep device state in a managed connection pool.

Recommended stack
-----------------

- **FastAPI** for HTTP
- **Uvicorn** as the ASGI server
- **SSE** for live capture streaming

Connection lifecycle
--------------------

The API should manage device connections with explicit connect/disconnect calls
and a short idle timeout. Each connection is keyed by ``device_id`` or
``ip:port``.

Proposed endpoints
------------------

Health
^^^^^^

- ``GET /health`` -> ``{ "status": "ok" }``

Devices
^^^^^^^

- ``POST /devices/connect``

Request:

.. code-block:: json

    {
      "ip": "192.168.1.201",
      "port": 4370,
      "timeout": 10,
      "password": 0,
      "force_udp": false,
      "encoding": "UTF-8"
    }

Response:

.. code-block:: json

    {
      "device_id": "192.168.1.201:4370",
      "serial": "0000000001",
      "fp_version": "10",
      "platform": "ZEM600_TFT"
    }

- ``POST /devices/disconnect``

Request:

.. code-block:: json

    { "device_id": "192.168.1.201:4370" }

Users
^^^^^

- ``GET /devices/{device_id}/users``
- ``POST /devices/{device_id}/users``
- ``DELETE /devices/{device_id}/users/{uid}``

Attendance
^^^^^^^^^^

- ``GET /devices/{device_id}/attendance``
- ``DELETE /devices/{device_id}/attendance``

Templates
^^^^^^^^^

- ``GET /devices/{device_id}/templates``
- ``GET /devices/{device_id}/templates/{uid}/{fid}``

Real-time events (SSE)
^^^^^^^^^^^^^^^^^^^^^^

- ``GET /devices/{device_id}/live``

SSE event payload:

.. code-block:: json

    {
      "type": "attendance",
      "user_id": "1001",
      "timestamp": "2024-06-01T12:00:00",
      "status": 0,
      "punch": 0
    }

Error model
-----------

All errors should return:

.. code-block:: json

    {
      "error": {
        "code": "DEVICE_OFFLINE",
        "message": "Device did not respond"
      }
    }

Security
--------

- Prefer network isolation and IP allowlists.
- Consider an API key or JWT for remote calls.
- The server should never expose device passwords in responses.

Open questions
--------------

- How to handle multiple concurrent clients reading attendance.
- Whether to expose raw template data or require an opt-in flag.
