"""
body.py - Blip's body. Expressive primitives, not raw hardware calls.

Everything reaches the robot through here, so when we learn a better way to do
something we fix it once. Nothing above this file imports cyberpi directly.
"""

import time


def keep_him_awake():
    """Release DTR/RTS on every serial open.

    Learned on hardware: with those lines asserted the ESP32 sits in reset -
    backlight on, screen blank, no menu, surviving a power cycle. Makeblock's
    library opens the port itself, so we patch pyserial underneath it.
    """
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


keep_him_awake()

try:
    import cyberpi
except ImportError:
    cyberpi = None

_DEAD = -1          # every strategy for this action failed; stop trying


class Body:
    """One robot, addressed the way a character would be, not a datasheet.

    The library's API shifts between firmware versions, so each action carries
    a few candidate strategies. We remember WHICH strategy worked - never a
    call with its arguments baked in, or he'd repeat one note forever.
    """

    def __init__(self, quiet=False):
        self.ok = cyberpi is not None
        self.quiet = quiet
        self._works = {}
        if self.ok:
            self._dispatch("online", [lambda: cyberpi.goto_online_mode()])

    def _dispatch(self, key, strategies, *args):
        """Run the first strategy that doesn't raise; remember the winner."""
        chosen = self._works.get(key)
        if chosen == _DEAD:
            return None
        if chosen is not None:
            try:
                return strategies[chosen](*args)
            except Exception:
                return None
        for index, strategy in enumerate(strategies):
            try:
                result = strategy(*args)
                self._works[key] = index
                return result
            except Exception:
                continue
        self._works[key] = _DEAD
        return None

    # -- identity ---------------------------------------------------------
    def firmware(self):
        if not self.ok:
            return None
        return self._dispatch("fw", [lambda: cyberpi.get_firmware_version()])

    def battery(self):
        if not self.ok:
            return None
        return self._dispatch("batt", [lambda: cyberpi.get_battery()])

    # -- face -------------------------------------------------------------
    def face(self, text, size=32):
        """His whole expression is one short string, centred and large."""
        if not self.ok:
            print(f"[face] {text}")
            return
        self._dispatch("face", [
            lambda t, s: cyberpi.display.show_label(t, s, "center"),
            lambda t, s: cyberpi.display.show_label(t, s, "center", 1),
            lambda t, s: cyberpi.console.println(t),
        ], text, size)

    def clear(self):
        if not self.ok:
            return
        self._dispatch("clear", [
            lambda: cyberpi.display.clear(),
            lambda: cyberpi.console.clear(),
        ])

    # -- lights -----------------------------------------------------------
    def glow(self, spec):
        """spec is 'red orange yellow green blue' or an (r, g, b) tuple."""
        if not self.ok:
            print(f"[glow] {spec}")
            return
        if isinstance(spec, (tuple, list)):
            r, g, b = spec
            self._dispatch("rgb", [lambda a, b_, c: cyberpi.led.on(a, b_, c)], r, g, b)
        else:
            self._dispatch("named", [lambda s: cyberpi.led.show(s)], spec)

    def dark(self):
        if not self.ok:
            return
        self._dispatch("off", [
            lambda: cyberpi.led.off(),
            lambda: cyberpi.led.on(0, 0, 0),
            lambda: cyberpi.led.show("black black black black black"),
        ])

    # -- voice ------------------------------------------------------------
    def tone(self, hz, seconds=0.15):
        """One note of his beep-language."""
        if self.quiet:
            time.sleep(seconds)
            return
        if not self.ok:
            print(f"[tone] {hz}Hz {seconds}s")
            time.sleep(seconds)
            return
        played = self._dispatch("tone", [
            lambda h, s: cyberpi.audio.play_tone(h, s),
            lambda h, s: cyberpi.audio.play_note(h, s),
        ], hz, seconds)
        if played is None and self._works.get("tone") == _DEAD:
            time.sleep(seconds)

    def rest(self, seconds):
        time.sleep(seconds)

    # -- senses -----------------------------------------------------------
    def loudness(self):
        if not self.ok:
            return None
        return self._dispatch("loud", [lambda: cyberpi.get_loudness()])

    def brightness(self):
        if not self.ok:
            return None
        return self._dispatch("bri", [lambda: cyberpi.get_bri()])

    def shaken(self):
        if not self.ok:
            return None
        return self._dispatch("shake", [lambda: cyberpi.get_shakeval()])
