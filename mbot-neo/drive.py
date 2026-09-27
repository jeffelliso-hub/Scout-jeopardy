#!/usr/bin/env python3
"""
drive.py - try every way of turning his wheels, one at a time.

get_shield() reported "none" while his chassis lights were plainly on, and
that call is known to misreport in cyberpi 0.0.7 - so we stop trusting it and
test the motors directly. Each attempt is announced before it runs and
followed by a pause, so whatever moves him can be identified by name.

    PUT HIM ON THE FLOOR with room ahead, then:
    python3 drive.py

Each move is small and slow, and he's stopped between attempts.
"""

import signal
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from blip.body import keep_him_awake

keep_him_awake()


class Timeout(Exception):
    pass


def _alarm(sig, frm):
    raise Timeout()


try:
    signal.signal(signal.SIGALRM, _alarm)
    HAVE_ALARM = True
except Exception:
    HAVE_ALARM = False


def attempt(number, description, fn, settle=1.5):
    print(f"\n  [{number}] {description}")
    if HAVE_ALARM:
        signal.alarm(8)
    try:
        fn()
        if HAVE_ALARM:
            signal.alarm(0)
        print("       sent - did he move?")
    except Timeout:
        print("       hung, no reply")
        return
    except Exception as e:
        if HAVE_ALARM:
            signal.alarm(0)
        print(f"       refused [{type(e).__name__}] {e}")
        return
    time.sleep(settle)


def main():
    try:
        import cyberpi
    except Exception as e:
        sys.exit(f"cyberpi will not import: {e}")

    try:
        cyberpi.goto_online_mode()
    except Exception as e:
        print(f"online mode failed: {e}")

    m = cyberpi.mbot2

    print("=" * 56)
    print("PUT HIM ON THE FLOOR. Starting in 5 seconds.")
    print("Watch him, and note the NUMBER shown when he moves.")
    print("=" * 56)
    time.sleep(5)

    # Highest-level first, then progressively closer to the motors, so if
    # only the low-level calls work we learn exactly where the break is.
    attempt(1, "mbot2.forward(50, 1)", lambda: m.forward(50, 1))
    attempt(2, "mbot2.straight(30)", lambda: m.straight(30))
    attempt(3, "mbot2.drive_power(40, -40)  then stop",
            lambda: (m.drive_power(40, -40), time.sleep(1), m.drive_power(0, 0)))
    attempt(4, "mbot2.drive_speed(60, -60)  then stop",
            lambda: (m.drive_speed(60, -60), time.sleep(1), m.drive_speed(0, 0)))
    attempt(5, "mbot2.EM_set_power(50, 'all')  then stop",
            lambda: (m.EM_set_power(50, "all"), time.sleep(1), m.EM_stop("all")))
    attempt(6, "mbot2.EM_set_speed(80, 'all')  then stop",
            lambda: (m.EM_set_speed(80, "all"), time.sleep(1), m.EM_stop("all")))
    attempt(7, "mbot2.motor_drive(50, -50)  then stop",
            lambda: (m.motor_drive(50, -50), time.sleep(1), m.motor_drive(0, 0)))
    attempt(8, "mbot2.turn_right(90)", lambda: m.turn_right(90))
    attempt(9, "mbot2.EM_turn(90, 'EM1')", lambda: m.EM_turn(90, "EM1"))

    # If the wheels turned at all, the encoders will have counted it, even
    # if we couldn't see it happen.
    print("\n" + "=" * 56)
    print("Encoder readings - these count actual wheel rotation:")
    for port in ("EM1", "EM2", 1, 2, "all"):
        try:
            print(f"  EM_get_angle({port!r}) = {m.EM_get_angle(port)}")
        except Exception as e:
            print(f"  EM_get_angle({port!r}) refused: {type(e).__name__}")

    try:
        m.EM_stop("all")
    except Exception:
        pass

    print("\nWhich NUMBER moved him? If none did, say so and tell me whether")
    print("any of them made a noise - a motor straining still counts.")


if __name__ == "__main__":
    main()
