# pyzk Roadmap

This roadmap tracks the next steps for pyzk. It is intentionally high level
and may change as new devices or protocol details are discovered.

## Now

- Complete the Sphinx documentation with real usage guides.
- Publish a supported backup/restore CLI (`pyzk-backup`) and helper API.
- Expand the compatible devices list and add a contribution template.

## Next

- Ship an HTTP REST API server (implementation of the spec in `docs/api_design.rst`).
- Provide a real-time streaming API (SSE or WebSocket) for live events.
- Add more example scripts for common tasks (backup, sync time, unlock door).

## Later

- Add automated compatibility tests for known devices.
- Expand device support for newer firmware families.
- Optional plugins for exporting data to common systems (CSV, database).
