#!/usr/bin/env python3
"""
move.py - can he actually drive?

get_battery() reported 0, and the wheels run off the chassis battery rather
than USB, so a still robot might mean flat batteries rather than wrong code.
This checks power first, then tries one small movement at a time.

    python3 move.py             # power check only, nothing moves
    python3 move.py --go        # PUT HIM ON THE FLOOR first
"""

import argparse
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from blip.body import Body
from blip import voice


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="actually move him")
    args = ap.parse_args()

    body = Body()
    if not body.ok:
        sys.exit("cyberpi not installed. Try: pip install cyberpi")

    print("Power")
    cyber = body.battery()
    chassis = body.extra_battery()
    shield = body.shield()
    print(f"  CyberPi battery : {cyber}")
    print(f"  chassis battery : {chassis}   <- the wheels run on this one")
    print(f"  shield          : {shield}")

    print("\nEyes")
    print(f"  distance ahead  : {body.distance()} cm")

    detached = (not shield) or str(shield).lower() in ("none", "0", "null")
    if detached:
        print("\n" + "!" * 56)
        print("HE IS NOT ATTACHED TO HIS BODY.")
        print("!" * 56)
        print("The CyberPi - the clear module with the screen - is one piece.")
        print("The blue chassis with the wheels, battery and ultrasonic eyes")
        print("is another. The brain cannot see the chassis right now, which")
        print("is why the battery reads 0, the eyes read 0 cm, and nothing")
        print("can drive.")
        print("")
        print("  1. Slide the CyberPi into the slot on the blue robot body.")
        print("  2. Switch the CHASSIS on - its own switch, not the CyberPi's.")
        print("  3. Charge the chassis battery if it has been sitting a while.")
        print("")
        print("Everything else works: screen, lights, speaker, microphone,")
        print("and the tilt and shake sensors are all in the brain itself.")
        return

    if not args.go:
        print("\nNothing moved. Put him on the floor, then: python3 move.py --go")
        return

    if not chassis:
        print("\n  WARNING: chassis battery reads empty or unavailable.")
        print("  If he doesn't move, charge him before we blame the code.")

    print("\nMoving. Watch him.")
    voice.say(body, "curious")

    print("  forward")
    body.ahead(30, 0.5)
    body.rest(0.8)

    print("  back")
    body.back(30, 0.5)
    body.rest(0.8)

    print("  turn right")
    body.spin(90)
    body.rest(0.8)

    print("  turn left")
    body.spin(-90)
    body.rest(0.8)

    body.halt()
    voice.say(body, "proud")
    print("\nWhich of those actually happened?")


if __name__ == "__main__":
    main()
