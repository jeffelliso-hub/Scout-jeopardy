"""
body.py - Blip's body. Expressive primitives, not raw hardware calls.

Everything reaches the robot through here, so when we learn a better way to do
something we fix it once. Nothing above this file imports cyberpi directly.
"""

import time


def keep_him_awake():
    """Open serial ports without ever resetting him.

    Two separate problems, both learned on hardware:

    1. Opening the port with DTR/RTS asserted pins the ESP32 in reset. The
       backlight stays lit, the screen goes blank, no menu, and it survives a
       power cycle. Recovery is unplug USB, then power cycle.
    2. Even a brief assertion while opening pulses reset, so he reboots at
       the start of every program.

    pyserial applies dtr/rts that were set while CLOSED at the moment it
    opens, so we build the port closed, silence both lines, then open. The
    patch sits under Makeblock's library, which opens ports itself.
    """
    try:
        import serial
    except ImportError:
        return False

    original = serial.Serial.__init__

    def patched(self, *args, **kwargs):
        port = kwargs.pop("port", None)
        if args:
            port, args = args[0], args[1:]

        original(self, None, *args, **kwargs)     # construct it closed

        try:
            self.dtr = False                      # queued until open
            self.rts = False
        except Exception:
            pass

        if port is not None:
            self.port = port
            try:
                self.dtr = False
                self.rts = False
            except Exception:
                pass
            self.open()

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

    # -- power ------------------------------------------------------------
    def extra_battery(self):
        """The chassis battery - the one the wheels actually run on."""
        if not self.ok:
            return None
        return self._dispatch("xbatt", [lambda: cyberpi.get_extra_battery()])

    def shield(self):
        if not self.ok:
            return None
        return self._dispatch("shield", [lambda: cyberpi.get_shield()])

    # -- motion -----------------------------------------------------------
    # His wheels are encoder motors on the mBot2 shield, reached through
    # cyberpi.mbot2. Speeds stay modest: he lives on tables and short cords.
    def ahead(self, speed=30, seconds=0.5):
        if not self.ok:
            print(f"[ahead] {speed} for {seconds}s")
            return
        self._dispatch("ahead", [
            lambda v, t: cyberpi.mbot2.forward(v, t),
            lambda v, t: cyberpi.mbot2.forward(v),
        ], speed, seconds)

    def back(self, speed=30, seconds=0.5):
        if not self.ok:
            print(f"[back] {speed} for {seconds}s")
            return
        self._dispatch("back", [
            lambda v, t: cyberpi.mbot2.backward(v, t),
            lambda v, t: cyberpi.mbot2.backward(v),
        ], speed, seconds)

    def spin(self, degrees=90):
        """Positive turns right, negative turns left."""
        if not self.ok:
            print(f"[spin] {degrees}")
            return
        if degrees >= 0:
            self._dispatch("right", [
                lambda d: cyberpi.mbot2.turn_right(d),
                lambda d: cyberpi.mbot2.turn(d),
            ], abs(degrees))
        else:
            self._dispatch("left", [
                lambda d: cyberpi.mbot2.turn_left(d),
                lambda d: cyberpi.mbot2.turn(-d),
            ], abs(degrees))

    def halt(self):
        if not self.ok:
            return
        self._dispatch("halt", [
            lambda: cyberpi.mbot2.EM_stop("all"),
            lambda: cyberpi.mbot2.EM_stop(),
            lambda: cyberpi.mbot2.drive_power(0, 0),
        ])

    # -- eyes -------------------------------------------------------------
    def distance(self):
        """Centimetres to whatever is in front of him, via the ultrasonic."""
        if not self.ok:
            return None
        return self._dispatch("dist", [
            lambda: cyberpi.ultrasonic2.get(1),
            lambda: cyberpi.ultrasonic2.get(),
        ])
