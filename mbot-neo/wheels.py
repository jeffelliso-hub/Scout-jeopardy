#!/usr/bin/env python3
"""
wheels.py - find out how to move him, by asking the robot instead of the docs.

His firmware version decides what the motion API is called, and guessing from
documentation has been unreliable. So: search the library for anything that
looks like motion, then try each one with a small nudge and watch which one
actually moves him.

    python3 wheels.py            # just list what exists (nothing moves)
    python3 wheels.py --test     # try each one - PUT HIM ON THE FLOOR

Each attempt is announced before it runs, so whatever twitches him, you'll
know its name.
"""

import argparse
import signal
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from blip.body import keep_him_awake

keep_him_awake()

MOTION_WORDS = ("forward", "backward", "turn", "drive", "motor", "speed",
                "em_", "move", "straight", "rotate", "wheel", "encoder")

# Argument shapes worth trying, loosest first. Small numbers on purpose:
# a brief, slow nudge tells us as much as a long one and travels less far.
ARG_SHAPES = [
    (30, 0.4),
    (30,),
    (0.4,),
    (30, 30),
    (30, 0.4, 0),
    (),
]


class Timeout(Exception):
    pass


def _alarm(sig, frm):
    raise Timeout()


try:
    signal.signal(signal.SIGALRM, _alarm)
    HAVE_ALARM = True
except Exception:
    HAVE_ALARM = False


def find_candidates(root, root_name, depth=1):
    """Callables whose names smell like motion, one level deep."""
    found = []
    for name in dir(root):
        if name.startswith("_"):
            continue
        try:
            obj = getattr(root, name)
        except Exception:
            continue
        label = f"{root_name}.{name}"
        if callable(obj) and any(w in name.lower() for w in MOTION_WORDS):
            found.append((label, obj))
        elif depth > 0 and not callable(obj) and hasattr(obj, "__class__"):
            if type(obj).__module__ not in ("builtins",):
                found.extend(find_candidates(obj, label, depth - 1))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="actually try them")
    args = ap.parse_args()

    try:
        import cyberpi
    except Exception as e:
        sys.exit(f"cyberpi will not import: {e}")

    candidates = find_candidates(cyberpi, "cyberpi")

    for extra in ("mbot2", "mbuild"):
        try:
            mod = __import__(extra)
            candidates.extend(find_candidates(mod, extra))
        except Exception:
            pass

    seen, unique = set(), []
    for label, fn in candidates:
        if label not in seen:
            seen.add(label)
            unique.append((label, fn))

    print(f"Found {len(unique)} things that might be his wheels:\n")
    for label, _fn in unique:
        print(f"  {label}")

    if not unique:
        print("\nNothing matched. Send me: python3 hello.py --api")
        return

    if not args.test:
        print("\nNothing was moved. Put him on the floor and run:")
        print("    python3 wheels.py --test")
        return

    try:
        cyberpi.goto_online_mode()
    except Exception:
        pass

    print("\n" + "=" * 56)
    print("PUT HIM ON THE FLOOR. Starting in 5 seconds.")
    print("Watch him. Note which name is on screen when he moves.")
    print("=" * 56)
    time.sleep(5)

    worked = []
    for label, fn in unique:
        for shape in ARG_SHAPES:
            call = f"{label}{shape}"
            print(f"\n  trying {call}")
            if HAVE_ALARM:
                signal.alarm(6)
            try:
                fn(*shape)
                if HAVE_ALARM:
                    signal.alarm(0)
                print("        accepted - did he move?")
                worked.append(call)
                time.sleep(1.2)
                break            # this shape fits; move to the next name
            except Timeout:
                print("        hung")
                break
            except TypeError:
                if HAVE_ALARM:
                    signal.alarm(0)
                continue         # wrong number of arguments, try another shape
            except Exception as e:
                if HAVE_ALARM:
                    signal.alarm(0)
                print(f"        rejected [{type(e).__name__}] {e}")
                break

    print("\n" + "=" * 56)
    print("Calls his firmware accepted:")
    for call in worked:
        print(f"  {call}")
    print("\nTell me WHICH ONE actually moved him - accepted only means he")
    print("didn't complain, not that the wheels turned.")


if __name__ == "__main__":
    main()
