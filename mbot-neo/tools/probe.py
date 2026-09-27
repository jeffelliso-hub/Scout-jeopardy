#!/usr/bin/env python3
"""
probe.py - reconnaissance on the CyberPi brain of an mBot Neo.

Answers one question: what does this board actually give us over USB,
without any Makeblock software in the loop?

Read-only. Touches nothing on the device, writes no files to it, and never
goes near firmware. Worst case it finds nothing and says so.

    pip install pyserial
    python3 tools/probe.py

Writes a report to probe-report.txt. Send that back and we'll know exactly
what we're building on.
"""

import argparse
import sys
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    sys.exit("Need pyserial first:\n\n    pip install pyserial\n")


BAUD = 115200
# Ports that are never the robot - bluetooth pseudo-ports, debug consoles.
PORT_NOISE = ("bluetooth", "debug-console", "wlan-debug")


def candidate_ports():
    """Every serial port that could plausibly be the robot, best guess first."""
    found = []
    for p in list_ports.comports():
        if any(n in p.device.lower() for n in PORT_NOISE):
            continue
        blob = " ".join(str(x) for x in (p.description, p.manufacturer, p.product)).lower()
        # CyberPi shows up behind one of the usual USB-serial bridges, or as
        # a plain CDC device. Rank the likely ones up.
        score = 0
        for hint, pts in (("cyberpi", 50), ("makeblock", 50), ("ch340", 20),
                          ("cp210", 20), ("usb serial", 10), ("usbmodem", 10),
                          ("ttyacm", 10), ("ttyusb", 8), ("wch", 8)):
            if hint in blob or hint in p.device.lower():
                score += pts
        found.append((score, p))
    found.sort(key=lambda t: -t[0])
    return [p for _, p in found]


class Repl:
    """Talks to MicroPython's raw REPL, which is the whole ballgame.

    If this connects, we own the board: we can run arbitrary code, read the
    filesystem, and push our own programs - with no vendor tooling at all.
    """

    def __init__(self, port, timeout=4):
        self.ser = serial.Serial(port, BAUD, timeout=timeout)
        self.banner = b""

    def close(self):
        try:
            self.ser.write(b"\r\x02")   # back to the friendly REPL, be polite
            self.ser.close()
        except Exception:
            pass

    def enter_raw(self):
        """Interrupt whatever is running and drop into raw REPL mode."""
        self.ser.reset_input_buffer()
        self.ser.write(b"\r\x03\x03")   # two Ctrl-C: stop any running program
        time.sleep(0.4)
        self.banner = self.ser.read(self.ser.in_waiting or 1)
        self.ser.reset_input_buffer()
        self.ser.write(b"\r\x01")       # Ctrl-A: raw REPL
        time.sleep(0.3)
        hello = self.ser.read(self.ser.in_waiting or 1)
        self.banner += hello
        return b"raw REPL" in hello

    def run(self, code):
        """Execute a snippet on the board. Returns (stdout, stderr)."""
        self.ser.reset_input_buffer()
        self.ser.write(code.encode() + b"\x04")   # Ctrl-D: execute
        if self.ser.read(2) != b"OK":
            return "", "device did not acknowledge"
        buf = b""
        deadline = time.time() + 12
        # Output ends with \x04 <traceback> \x04 >
        while buf.count(b"\x04") < 2 and time.time() < deadline:
            chunk = self.ser.read(self.ser.in_waiting or 1)
            if chunk:
                buf += chunk
            else:
                time.sleep(0.02)
        out, _, rest = buf.partition(b"\x04")
        err, _, _ = rest.partition(b"\x04")
        return out.decode(errors="replace").strip(), err.decode(errors="replace").strip()


# Each probe is (label, code). Kept small and independent so one failure
# never hides the next answer.
PROBES = [
    ("micropython", "import sys; print(sys.implementation)"),
    ("platform",    "import sys; print(sys.platform)"),
    ("board",       "import os; print(os.uname())"),
    ("free_ram",    "import gc; gc.collect(); print(gc.mem_free())"),
    ("root_fs",     "import os; print(os.listdir('/'))"),
    ("disk_free",   "import os; s=os.statvfs('/'); print(s[0]*s[3], 'bytes free')"),
    ("modules",     "help('modules')"),
    # The libraries that decide what he can become:
    ("cyberpi",     "import cyberpi; print('yes')"),
    ("cyberpi_api", "import cyberpi; print(sorted(a for a in dir(cyberpi) if not a.startswith('_')))"),
    ("audio",       "import cyberpi; print(sorted(a for a in dir(cyberpi.audio) if not a.startswith('_')))"),
    ("wifi",        "import cyberpi; print([a for a in dir(cyberpi) if 'wifi' in a.lower() or 'cloud' in a.lower() or 'net' in a.lower()])"),
    ("mbot2",       "import mbot2; print(sorted(a for a in dir(mbot2) if not a.startswith('_')))"),
    ("mbuild",      "import mbuild; print(sorted(a for a in dir(mbuild) if not a.startswith('_')))"),
    ("urequests",   "import urequests; print('yes')"),
    ("ujson",       "import ujson; print('yes')"),
    ("socket",      "import usocket; print('yes')"),
]


def main():
    ap = argparse.ArgumentParser(description="Probe a CyberPi / mBot Neo over USB serial.")
    ap.add_argument("--port", help="serial port; auto-detected if omitted")
    ap.add_argument("--out", default="probe-report.txt")
    args = ap.parse_args()

    lines = []

    def say(s=""):
        print(s)
        lines.append(s)

    say("mBot Neo / CyberPi probe")
    say("=" * 60)

    ports = candidate_ports()
    say("\nSerial ports visible:")
    if not ports:
        say("  (none)")
    for p in ports:
        say(f"  {p.device}  |  {p.description}  |  vid:pid={p.vid}:{p.pid}")

    targets = [args.port] if args.port else [p.device for p in ports]
    if not targets:
        say("\nNo serial ports at all. Is he plugged in with a DATA cable")
        say("(not a charge-only one) and powered on?")
        write_report(args.out, lines)
        return 1

    found = False
    for port in targets:
        if found:
            break
        say(f"\n--- trying {port} ---")
        try:
            repl = Repl(port)
        except Exception as e:
            say(f"  could not open: {e}")
            continue

        try:
            if not repl.enter_raw():
                say("  No MicroPython raw REPL here.")
                say(f"  Raw bytes the port sent us: {repl.banner[:200]!r}")
                say("  (That dump is still useful - it tells us what protocol it IS speaking.)")
                continue

            found = True
            say("  RAW REPL FOUND. We own this board.\n")
            for label, code in PROBES:
                out, err = repl.run(code)
                if err:
                    first = err.strip().splitlines()[-1] if err.strip() else "error"
                    say(f"  {label:<13} -- {first}")
                else:
                    text = out if len(out) < 1500 else out[:1500] + " ...(truncated)"
                    say(f"  {label:<13} : {text}")
            say("\n  Nothing was written to the device.")
        finally:
            repl.close()

    if not found:
        say("\nNo MicroPython REPL on any port. Not fatal - the raw-byte dumps")
        say("above tell us what the firmware is speaking instead.")
    write_report(args.out, lines)
    return 0


def write_report(path, lines):
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"\nReport saved to {path} - send me that file.")


if __name__ == "__main__":
    sys.exit(main())
