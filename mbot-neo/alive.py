#!/usr/bin/env python3
"""
alive.py - Blip, living in your room. Ctrl-C to stop.

No script, no sequence. He reads the room several times a second and decides
what to do about it, and his mood carries over from the last time you ran
this - so he knows whether you've been gone ten minutes or two days.

    PUT HIM ON THE FLOOR with some space.
    python3 alive.py
    python3 alive.py --still     # react, but never drive (desk-safe)

Things worth trying: walk up to him, walk away and leave him alone for a
few minutes, pick him up, shout near him, turn the lights off.
"""

import argparse
import random
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from blip.body import Body
from blip.mood import Mood
from blip import voice

NEAR_CM = 30           # closer than this and he considers you present
LOUD = 45              # loudness that counts as a shout
DARK = 12              # below this he thinks the lights are off
TICK = 0.45            # seconds between looks at the world


class Blip:
    def __init__(self, body, mood, still=False):
        self.body = body
        self.mood = mood
        self.still = still
        self.person_here = False
        self.last_wander = time.time()
        self.last_mood_shown = None

    # -- helpers -----------------------------------------------------------
    def drive(self, action, *args):
        if self.still:
            return
        action(*args)

    def show_mood(self):
        """Only repaint when the feeling actually changes - less flicker."""
        feeling = self.mood.feeling()
        if feeling != self.last_mood_shown:
            self.body.glow(self.mood.colour())
            self.last_mood_shown = feeling

    # -- the loop ----------------------------------------------------------
    def tick(self):
        distance = self.body.distance()
        loudness = self.body.loudness()
        light = self.body.brightness()
        shake = self.body.shaken()

        # --- being handled beats everything else -------------------------
        if shake is not None and shake > 30:
            rough = shake > 70
            self.mood.was_handled(rough=rough)
            voice.say(self.body, "hurt" if rough else "startled")
            self.show_mood()
            return

        # --- a shout -------------------------------------------------------
        if loudness is not None and loudness > LOUD:
            self.mood.was_startled()
            voice.say(self.body, "startled")
            self.drive(self.body.back, 35, 0.35)
            self.show_mood()
            return

        # --- someone arrives ----------------------------------------------
        near = distance is not None and 0 < distance < NEAR_CM
        if near and not self.person_here:
            self.person_here = True
            # Read the clock BEFORE meeting resets it, or he always thinks
            # you just left and is never pleased to see you.
            phrase, why = self.mood.greeting()
            missed_you = self.mood.saw_someone()
            print(f"    someone's here - {why}")
            voice.say(self.body, "delighted" if missed_you else phrase)
            if missed_you:
                self.drive(self.body.spin, 360)
            self.show_mood()
            return

        if not near and self.person_here:
            self.person_here = False
            print("    they left")
            voice.say(self.body, "goodbye")
            return

        # --- someone is still here ----------------------------------------
        if near:
            # Too close for comfort - he shuffles back.
            if distance < 10:
                self.drive(self.body.back, 25, 0.25)
            elif random.random() < 0.05:
                voice.say(self.body, "curious")
                self.mood.played()
            return

        # --- lights out -----------------------------------------------------
        if light is not None and light < DARK and self.mood.energy < 50:
            voice.say(self.body, "sleepy")
            self.mood.energy = min(100, self.mood.energy + 3)
            self.show_mood()
            time.sleep(2)
            return

        # --- bored, and nobody around ---------------------------------------
        if self.mood.boredom > 70 and time.time() - self.last_wander > 8:
            self.last_wander = time.time()
            print("    bored - going looking")
            voice.say(self.body, "bored")
            if distance is None or distance > 40:
                self.drive(self.body.ahead, 25, 0.5)
            self.drive(self.body.spin, random.choice([-60, 60, 90]))
            self.mood.wandered()
            self.show_mood()
            return

        # --- pestering --------------------------------------------------------
        if self.mood.boredom > 88 and random.random() < 0.15:
            voice.say(self.body, "pester")
            return

        self.show_mood()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", action="store_true", help="never drive")
    ap.add_argument("--name", help="rename him, permanently")
    args = ap.parse_args()

    body = Body()
    if not body.ok:
        sys.exit("cyberpi not installed. Try: pip install cyberpi")

    mood = Mood.load()
    if args.name:
        mood.name = args.name

    print(mood.summary())
    phrase, why = mood.greeting()
    print(f"waking up - {why}\n")

    body.face(mood.name)
    voice.say(body, phrase, show_face=False)
    body.rest(0.6)

    blip = Blip(body, mood, still=args.still)
    blip.show_mood()

    try:
        while True:
            blip.tick()
            time.sleep(TICK)
    except KeyboardInterrupt:
        print("\n\nstopping")
    finally:
        # Never walk away leaving his motors running.
        try:
            body.halt()
        except Exception:
            pass
        voice.say(body, "goodbye")
        body.dark()
        mood.save()
        print(mood.summary())
        print(f"\nremembered in ~/.blip/mood.json - he'll know how long you were gone")


if __name__ == "__main__":
    main()
