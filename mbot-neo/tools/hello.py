#!/usr/bin/env python3
"""
hello.py - first contact with the robot over Makeblock's serial protocol.

What probe3 taught us:
  * CyberPi speaks the Halocode protocol (0xf3-framed packets).
  * The library finds the board by the CH340 id 1A86:7523 - the port we found.
  * There is a goto_online_mode(), and live commands very likely need it first.

So: switch him online, prove a round trip with get_firmware_version() (we
already know the true answer is 44.01.009, which makes it a real test), then
try to make him visibly do something.

Every call is timeout-guarded, so one unsupported API cannot stop the rest.

    pip install cyberpi pyserial
    python3 hello.py            # lights, screen, sound, senses
    python3 hello.py --move     # also nudge the wheels (put him on the floor)
    python3 hello.py --api      # also dump the library's API surface
"""

import argparse
import os
import re
import signal
import sys

KNOWN_FIRMWARE = "44.01.009"     # from the boot banner probe2 caught

# ---------------------------------------------------------------------------
# Keep him awake.
#
# Opening this port with DTR/RTS asserted pins the ESP32's reset line and the
# board sits there switched off - backlight on, screen blank, no menu. We hit
# exactly that. Makeblock's library opens the port itself, so we patch
# pyserial underneath it to release both lines the moment any port opens.
# ---------------------------------------------------------------------------
def _keep_him_awake():
    try:
        import serial
    except ImportError:
        return False
    original = serial.Serial.__init__

    def patched(self, *args, **kwargs):
        original(self, *args, **kwargs)
        try:
            self.dtr = False
            self.rts = False
        except Exception:
            pass

    serial.Serial.__init__ = patched
    return True




class Timeout(Exception):
    pass


def _on_alarm(signum, frame):
    raise Timeout()


try:
    signal.signal(signal.SIGALRM, _on_alarm)
    HAVE_ALARM = True
except Exception:
    HAVE_ALARM = False


def guarded(label, fn, secs=10):
    if HAVE_ALARM:
        signal.alarm(secs)
    try:
        result = fn()
        if HAVE_ALARM:
            signal.alarm(0)
        print(f"  OK    {label}" + (f"  -> {result!r}" if result is not None else ""))
        return True, result
    except Timeout:
        print(f"  HANG  {label}  (silent for {secs}s)")
        return False, None
    except Exception as e:
        if HAVE_ALARM:
            signal.alarm(0)
        print(f"  FAIL  {label}  [{type(e).__name__}] {e}")
        return False, None


def dump_api(cyberpi):
    print("\n" + "=" * 60)
    print("Library API")
    print("=" * 60)
    names = sorted(a for a in dir(cyberpi) if not a.startswith("_"))
    print(f"\ncyberpi top level ({len(names)}):")
    for i in range(0, len(names), 6):
        print("  " + "  ".join(f"{n:<22}" for n in names[i:i + 6]))

    for sub in ("display", "led", "audio", "console", "controller", "cloud",
                "event", "chart", "barchart", "button", "humiture"):
        obj = getattr(cyberpi, sub, None)
        if obj is not None:
            subnames = sorted(a for a in dir(obj) if not a.startswith("_"))
            print(f"\ncyberpi.{sub}: {subnames}")

    try:
        print(f"\n----- {cyberpi.__file__} -----")
        print(open(cyberpi.__file__).read())
    except Exception as e:
        print(f"  (could not read shim: {e})")

    try:
        import makeblock
        api = os.path.join(os.path.dirname(makeblock.__file__),
                           "modules", "cyberpi", "api_cyberpi_api.py")
        sigs = re.findall(r"^\s*def\s+(\w+\s*\([^)]*\))", open(api).read(), re.M)
        print(f"\n----- {len(sigs)} functions in api_cyberpi_api.py -----")
        for s in sigs[:300]:
            print("  " + " ".join(s.split()))
    except Exception as e:
        print(f"  (could not read api file: {e})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--move", action="store_true", help="also nudge the wheels")
    ap.add_argument("--api", action="store_true", help="dump the API surface")
    ap.add_argument("--no-patch", action="store_true",
                    help="do not suppress DTR/RTS (he may sit in reset)")
    args = ap.parse_args()

    if not args.no_patch:
        print("holding DTR/RTS low so the port cannot reset him" if _keep_him_awake()
              else "pyserial missing - cannot protect against the reset line")

    try:
        import cyberpi
    except Exception as e:
        sys.exit(f"cyberpi will not import: {e}\n\nTry: pip install cyberpi")
    print(f"cyberpi loaded from {cyberpi.__file__}")

    if args.api:
        dump_api(cyberpi)

    # ---- wake the link -----------------------------------------------------
    print("\nHandshake")
    guarded("goto_online_mode", lambda: cyberpi.goto_online_mode(), secs=15)

    ok, ver = guarded("get_firmware_version", lambda: cyberpi.get_firmware_version(), secs=15)
    if ok and ver:
        match = "MATCHES the boot banner" if KNOWN_FIRMWARE in str(ver) else \
                f"expected {KNOWN_FIRMWARE}"
        print(f"        round trip is REAL - {match}")
    guarded("get_name", lambda: cyberpi.get_name())
    guarded("get_battery", lambda: cyberpi.get_battery())

    # ---- screen ------------------------------------------------------------
    print("\nScreen  (watch his display)")
    guarded("display.show_label", lambda: cyberpi.display.show_label("BLIP", 16, "center"))
    guarded("console.println", lambda: cyberpi.console.println("hello"))

    # ---- lights ------------------------------------------------------------
    print("\nLights  (watch the LED strip)")
    guarded("led.on(red)", lambda: cyberpi.led.on(255, 0, 0))
    guarded("led.show", lambda: cyberpi.led.show("red orange yellow green blue"))

    # ---- sound -------------------------------------------------------------
    print("\nSound  (listen)")
    guarded("audio.play('hello')", lambda: cyberpi.audio.play("hello"))
    guarded("audio.play_tone", lambda: cyberpi.audio.play_tone(523, 0.3))

    # ---- senses ------------------------------------------------------------
    print("\nSenses  (these are what make instincts possible)")
    for call in ("get_loudness", "get_bri", "get_shakeval", "get_roll",
                 "get_pitch", "get_yaw"):
        fn = getattr(cyberpi, call, None)
        if fn is None:
            print(f"  --    {call} not present")
        else:
            guarded(call, fn)

    # ---- wheels ------------------------------------------------------------
    if args.move:
        print("\nWheels  (he should twitch forward, then back)")
        moved = False
        for name in ("mbot2", "mbuild"):
            mod = getattr(cyberpi, name, None)
            if mod is not None and hasattr(mod, "forward"):
                guarded(f"{name}.forward", lambda m=mod: m.forward(30, 0.4))
                guarded(f"{name}.backward", lambda m=mod: m.backward(30, 0.4))
                moved = True
        if not moved:
            print("  --    no forward() found on cyberpi; run with --api and")
            print("        I'll find the right call for the wheels")
    else:
        print("\nWheels  skipped - add --move once he's on the floor")

    print("\nDone. Tell me what you SAW and HEARD, not just what printed.")
    print("If his screen went blank, unplug the USB and power cycle - that")
    print("restores him, and it means the reset line is still winning.")


if __name__ == "__main__":
    main()
