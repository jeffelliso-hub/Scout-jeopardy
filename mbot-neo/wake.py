#!/usr/bin/env python3
"""
wake.py - Blip wakes up.

The first thing he does that isn't a test. Run it and watch him come to life:
he stirs, notices the room, greets you, and settles.

    source ~/blip/bin/activate
    python3 wake.py
    python3 wake.py --quiet     # same, without the beeping
"""

import argparse
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from blip.body import Body
from blip import voice


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="no sound")
    ap.add_argument("--name", default="BLIP")
    args = ap.parse_args()

    body = Body(quiet=args.quiet)
    if not body.ok:
        sys.exit("cyberpi not installed here. Try: pip install cyberpi")

    # --- stirring --------------------------------------------------------
    body.dark()
    body.face("_   _")
    voice.say(body, "waking")
    body.glow((40, 20, 60))
    body.rest(0.4)

    # --- noticing the room -----------------------------------------------
    voice.say(body, "curious")
    light = body.brightness()
    noise = body.loudness()
    body.rest(0.3)

    # He reacts to what he finds, which is the whole point of having senses.
    if light is not None and light < 15:
        voice.say(body, "sleepy")
        body.glow((80, 60, 10))
        body.face("-   -")
    elif noise is not None and noise > 40:
        voice.say(body, "startled")
        body.glow((255, 120, 0))
    else:
        voice.say(body, "hello")
        body.glow("red orange yellow green blue")

    body.rest(0.5)

    # --- saying his name -------------------------------------------------
    body.face(args.name)
    voice.say(body, "proud", show_face=False)
    body.rest(0.6)

    # --- settling --------------------------------------------------------
    body.glow((0, 60, 90))
    body.face("^   ^")

    print("\nHe's awake.")
    print(f"  firmware : {body.firmware()}")
    print(f"  battery  : {body.battery()}")
    print(f"  light    : {light}")
    print(f"  loudness : {noise}")
    print(f"\nHis vocabulary so far: {', '.join(voice.vocabulary())}")
    print("\nTry:  python3 wake.py --name SCOUT")


if __name__ == "__main__":
    main()
