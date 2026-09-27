#!/usr/bin/env python3
"""
probe3.py - study Makeblock's own host-side library to learn the wire protocol.

probe2 proved the firmware is a compiled ESP-IDF app (v44.01.009), not
MicroPython, so there's no REPL to talk to. But Makeblock publishes the
computer side of their serial protocol on PyPI as `cyberpi`. This inspects
that package so we can write our OWN client and ship no vendor code in Blip.

    pip install cyberpi
    python3 probe3.py

Inspection only - it does not connect to the robot or send him anything.
"""

import importlib
import os
import sys
import traceback

# Files whose names suggest they carry the framing/transport logic.
JUICY = ("protocol", "serial", "link", "transport", "packet", "frame",
         "connect", "comm", "port", "bus", "sender", "receiver", "board")
MAX_DUMP_LINES = 160
MAX_FILES_DUMPED = 6


def header(s):
    print(f"\n{'=' * 64}\n{s}\n{'=' * 64}")


def try_import(name):
    try:
        mod = importlib.import_module(name)
        return mod, None
    except Exception:
        return None, traceback.format_exc(limit=3).strip()


def tree(root):
    """Every .py in the package, with size, shortest paths first."""
    out = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".py"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root)
                try:
                    size = os.path.getsize(full)
                except OSError:
                    size = -1
                out.append((rel, size, full))
    out.sort(key=lambda t: (t[0].count(os.sep), t[0]))
    return out


def dump(path, rel):
    print(f"\n----- {rel} -----")
    try:
        with open(path, "r", errors="replace") as fh:
            lines = fh.read().splitlines()
    except Exception as e:
        print(f"  (unreadable: {e})")
        return
    for line in lines[:MAX_DUMP_LINES]:
        print("  " + line)
    if len(lines) > MAX_DUMP_LINES:
        print(f"  ... ({len(lines) - MAX_DUMP_LINES} more lines)")


def main():
    header("Environment")
    print(f"python  : {sys.version.split()[0]}")
    print(f"platform: {sys.platform}")

    found = {}
    for name in ("cyberpi", "makeblock", "mbuild", "mbot2"):
        mod, err = try_import(name)
        if mod is None:
            print(f"\n{name:<10}: NOT IMPORTABLE")
            print("   " + (err or "").replace("\n", "\n   ")[:400])
            continue
        loc = getattr(mod, "__file__", None) or "(namespace package)"
        ver = getattr(mod, "__version__", "?")
        print(f"\n{name:<10}: {loc}  (version {ver})")
        found[name] = mod
        api = sorted(a for a in dir(mod) if not a.startswith("_"))
        print(f"   top-level names: {api[:40]}")

    if not found:
        header("Nothing to inspect")
        print("Install it first:   pip install cyberpi")
        return 1

    for name, mod in found.items():
        f = getattr(mod, "__file__", None)
        if not f:
            continue
        root = os.path.dirname(f)
        header(f"{name} - file tree ({root})")
        files = tree(root)
        for rel, size, _full in files:
            print(f"  {size:>7}  {rel}")

        picks = [(rel, full) for rel, _s, full in files
                 if any(k in rel.lower() for k in JUICY)][:MAX_FILES_DUMPED]
        if picks:
            header(f"{name} - likely protocol source")
            for rel, full in picks:
                dump(full, rel)

    header("Done")
    print("Nothing was sent to the robot. Paste this output back.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
