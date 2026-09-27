#!/usr/bin/env python3
"""
hello.py - first contact. Try to make the robot visibly do something.

Uses Makeblock's own `cyberpi` package over USB. Every call is guarded by a
timeout and a try/except, so one broken API can't stop the rest - the point
is to learn which calls this firmware actually honours.

    pip install cyberpi pyserial
    python3 hello.py            # lights, screen, sound, sensors
    python3 hello.py --move     # also nudge the wheels (put him on the floor)

Without --move he does not drive. Nothing is written to his filesystem.
"""

import argparse
import signal
import sys

try:
    from serial.tools import list_ports
except ImportError:
    list_ports = None


class Timeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise Timeout()


try:
    signal.signal(signal.SIGALRM, _on_alarm)
    HAVE_ALARM = True
except Exception:
    HAVE_ALARM = False


def guarded(label, fn, secs=8):
    """Run fn, surviving hangs and exceptions alike. Returns (ok, result)."""
    if HAVE_ALARM:
        signal.alarm(secs)
    try:
        result = fn()
        if HAVE_ALARM:
            signal.alarm(0)
        print(f"  OK    {label}" + (f"  -> {result!r}" if result is not None else ""))
        return True, result
    except Timeout:
        print(f"  HANG  {label}  (no response in {secs}s)")
        return False, None
    except Exception as e:
        if HAVE_ALARM:
            signal.alarm(0)
        print(f"  FAIL  {label}  [{type(e).__name__}] {e}")
        return False, None


def show_ports():
    if not list_ports:
        print("  (pyserial missing - skipping port list)")
        return
    for p in list_ports.comports():
        mark = " <-- CH340, this is him" if (p.vid, p.pid) == (0x1A86, 0x7523) else ""
        print(f"  {p.device}  vid:pid={p.vid}:{p.pid}{mark}")


def describe(name, mod):
    """Print a module's public API so we learn what this firmware offers."""
    names = sorted(a for a in dir(mod) if not a.startswith("_"))
    print(f"\n  {name} ({len(names)}): {names}")
    for sub in ("display", "led", "audio", "console", "controller", "wifi", "cloud"):
        obj = getattr(mod, sub, None)
        if obj is not None:
            subnames = sorted(a for a in dir(obj) if not a.startswith("_"))
            print(f"    .{sub}: {subnames}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--move", action="store_true", help="also nudge the wheels")
    args = ap.parse_args()

    print("Serial ports")
    show_ports()

    print("\nImporting")
    try:
        import cyberpi
        print(f"  OK    cyberpi from {cyberpi.__file__}")
    except Exception as e:
        sys.exit(f"  FAIL  cyberpi: {e}\n\nTry: pip install cyberpi")

    describe("cyberpi", cyberpi)

    mbot2 = None
    try:
        import mbot2
        print(f"\n  OK    mbot2 from {mbot2.__file__}")
        describe("mbot2", mbot2)
    except Exception as e:
        print(f"\n  note  mbot2 not importable: {e}")

    # ---- screen -----------------------------------------------------------
    print("\nScreen  (watch his display)")
    guarded("display.show_label", lambda: cyberpi.display.show_label("BLIP", 16, "center"))
    guarded("console.println", lambda: cyberpi.console.println("hello"))

    # ---- lights -----------------------------------------------------------
    print("\nLights  (watch the LED strip)")
    guarded("led.on(red)", lambda: cyberpi.led.on(255, 0, 0))
    guarded("led.show", lambda: cyberpi.led.show("red orange yellow green blue"))
    guarded("led.off", lambda: cyberpi.led.off())

    # ---- sound ------------------------------------------------------------
    print("\nSound  (listen)")
    guarded("audio.play('hello')", lambda: cyberpi.audio.play("hello"))
    guarded("audio.play_tone", lambda: cyberpi.audio.play_tone(523, 0.3))
    guarded("audio.play_melody", lambda: cyberpi.audio.play_melody("up"))

    # ---- senses -----------------------------------------------------------
    print("\nSenses  (reading these is what makes instincts possible)")
    for call in ("get_battery", "get_loudness", "get_bri", "get_shakeval",
                 "get_roll", "get_pitch", "get_yaw"):
        fn = getattr(cyberpi, call, None)
        if fn is None:
            print(f"  --    {call} not present")
            continue
        guarded(call, fn)

    # ---- wheels -----------------------------------------------------------
    if args.move and mbot2:
        print("\nWheels  (he should twitch forward then back)")
        guarded("forward", lambda: mbot2.forward(30, 0.4))
        guarded("backward", lambda: mbot2.backward(30, 0.4))
    elif mbot2:
        print("\nWheels  skipped - pass --move when he's on the floor")

    print("\nDone. Tell me what you actually saw and heard.")


if __name__ == "__main__":
    main()
