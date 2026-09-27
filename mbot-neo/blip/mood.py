"""
mood.py - the part of Blip that survives being switched off.

A robot that boots blank every time can never be a pet. It can only ever be
a program that runs. So his inner state lives in a file: how rested he is,
how cheerful, how curious, how bored, and how much he trusts whoever is in
front of him - plus when he last saw anyone.

This lives on the computer for now. When we can write to his own filesystem
it moves onto the board, and then he remembers on battery in another room.
"""

import json
import os
import time

HOME = os.path.expanduser("~/.blip")
PATH = os.path.join(HOME, "mood.json")

# How fast each feeling drifts back toward its resting value, per minute
# alone. Boredom climbs, everything else sags.
DRIFT = {
    "energy": +0.6,      # resting recovers him
    "cheer": -0.4,       # being alone slowly flattens him
    "curiosity": +0.8,   # curiosity rebuilds when nothing has happened
    "boredom": +1.8,     # and boredom builds fastest of all
}

FLOOR, CEILING = 0.0, 100.0


def _clamp(value):
    return max(FLOOR, min(CEILING, value))


class Mood:
    def __init__(self, **state):
        self.name = state.get("name", "BLIP")
        self.energy = state.get("energy", 80.0)
        self.cheer = state.get("cheer", 60.0)
        self.curiosity = state.get("curiosity", 70.0)
        self.boredom = state.get("boredom", 20.0)
        self.trust = state.get("trust", 50.0)       # grows slowly, never drifts
        self.last_seen = state.get("last_seen", 0.0)
        self.meetings = state.get("meetings", 0)
        self.awakenings = state.get("awakenings", 0)

    # -- persistence ------------------------------------------------------
    @classmethod
    def load(cls):
        try:
            with open(PATH) as fh:
                mood = cls(**json.load(fh))
        except Exception:
            mood = cls()
        mood._drift()
        mood.awakenings += 1
        return mood

    def save(self):
        os.makedirs(HOME, exist_ok=True)
        tmp = PATH + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(self.__dict__, fh, indent=2)
        os.replace(tmp, PATH)      # never leave a half-written brain behind

    # -- the passage of time ----------------------------------------------
    def _drift(self):
        """Apply however long he's been alone since anyone last saw him."""
        if not self.last_seen:
            return
        minutes = (time.time() - self.last_seen) / 60.0
        if minutes <= 0:
            return
        for field, rate in DRIFT.items():
            setattr(self, field, _clamp(getattr(self, field) + rate * minutes))

    def alone_for(self):
        """Minutes since he last saw a person. None if he never has."""
        if not self.last_seen:
            return None
        return (time.time() - self.last_seen) / 60.0

    # -- events -----------------------------------------------------------
    def saw_someone(self):
        first_in_a_while = (self.alone_for() or 999) > 10
        self.last_seen = time.time()
        self.meetings += 1
        self.boredom = _clamp(self.boredom - 35)
        self.cheer = _clamp(self.cheer + (18 if first_in_a_while else 6))
        self.trust = _clamp(self.trust + 0.8)
        return first_in_a_while

    def was_startled(self):
        self.cheer = _clamp(self.cheer - 8)
        self.energy = _clamp(self.energy - 4)
        self.curiosity = _clamp(self.curiosity + 5)

    def was_handled(self, rough=False):
        self.energy = _clamp(self.energy - 6)
        if rough:
            self.cheer = _clamp(self.cheer - 14)
            self.trust = _clamp(self.trust - 2)
        else:
            self.cheer = _clamp(self.cheer + 4)
            self.trust = _clamp(self.trust + 1.5)

    def played(self):
        self.boredom = _clamp(self.boredom - 25)
        self.cheer = _clamp(self.cheer + 10)
        self.energy = _clamp(self.energy - 8)
        self.trust = _clamp(self.trust + 2)

    def wandered(self):
        self.boredom = _clamp(self.boredom - 8)
        self.energy = _clamp(self.energy - 3)

    # -- how he reads ------------------------------------------------------
    def feeling(self):
        """One word for how he is. Order matters - strongest need wins."""
        if self.energy < 20:
            return "sleepy"
        if self.boredom > 75:
            return "bored"
        if self.cheer < 25:
            return "grumpy"
        if self.curiosity > 70:
            return "curious"
        if self.cheer > 75:
            return "happy"
        return "content"

    def colour(self):
        return {
            "sleepy": (60, 40, 10),
            "bored": (70, 40, 90),
            "grumpy": (120, 30, 0),
            "curious": (0, 90, 120),
            "happy": (0, 140, 60),
            "content": (0, 60, 90),
        }[self.feeling()]

    def greeting(self):
        """What he'd say about how long it's been, if he had words."""
        alone = self.alone_for()
        if alone is None:
            return "hello", "we have never met"
        if alone < 2:
            return "hey", "you only just left"
        if alone < 60:
            return "hello", f"alone for {int(alone)} minutes"
        if alone < 60 * 24:
            return "happy", f"alone for {int(alone / 60)} hours"
        return "delighted", f"alone for {int(alone / 1440)} days"

    def summary(self):
        return (f"{self.name}: {self.feeling()}  "
                f"energy {self.energy:.0f}  cheer {self.cheer:.0f}  "
                f"curiosity {self.curiosity:.0f}  bored {self.boredom:.0f}  "
                f"trust {self.trust:.0f}  met you {self.meetings}x")
