# Codex Agent Guide (pyzk)

## Repo overview
- `zk/` is the library package. The main entry point is `ZK` in `zk/base.py`.
- `example/` contains minimal usage scripts.
- `test_machine.py` and `test_backup_restore.py` are hardware-facing CLIs.
- `docs/` is a Sphinx site (ReadTheDocs compatible).

## Key modules
- `zk/base.py`: core protocol, connection handling, and device operations.
- `zk/user.py`: `User` model and packing helpers.
- `zk/finger.py`: `Finger` model and template packing helpers.
- `zk/attendance.py`: `Attendance` model.
- `zk/const.py`: protocol constants and flags.
- `zk/exception.py`: library exceptions.

## Safety notes
- Destructive calls include `clear_data()`, `clear_attendance()`, `poweroff()`, and `restart()`.
- `unlock()` opens the door/relay on some devices. Treat it as a safety-sensitive operation.
- Prefer `disable_device()` before bulk reads/writes to avoid inconsistent data.
- Live capture (`live_capture()`) can hold device state; ensure you exit cleanly.

## Common commands
- Run an example: `python example/get_users.py` (edit IP/port inside the script).
- Basic device probe: `python test_machine.py -a 192.168.1.201`.
- Backup/restore CLI (new): `pyzk-backup --help`.

## Docs build
- Build Sphinx docs: `cd docs && make html`.
- Or: `sphinx-build -b html docs docs/_build/html`.

## Hardware-dependent tests
- Any command that connects to a real device requires a reachable IP/port (default 4370).
- Use `--force-udp` if TCP is unreliable for a specific model.
- Time sync and firmware reads may differ by model/firmware version.

## Conventions
- Keep new code Python 2/3 compatible unless explicitly dropping support.
- Avoid changing protocol details without referencing `docs/_static/Communication_protocol_manual_CMD.pdf`.
