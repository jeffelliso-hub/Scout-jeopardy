#!/usr/bin/env python3
"""
check.py - is the brain talking to the body? Eight lines, no wall of text.

Everything on the CyberPi works; everything on the chassis reads zero. This
asks the few questions that separate "not plugged in properly" from "the
firmware won't drive this shield".
"""

import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from blip.body import keep_him_awake

keep_him_awake()

import cyberpi


def ask(label, fn):
    try:
        return f"{label}: {fn()!r}"
    except Exception as e:
        return f"{label}: refused ({type(e).__name__})"


try:
    cyberpi.goto_online_mode()
except Exception:
    pass

m = cyberpi.mbot2
lines = []

lines.append(ask("firmware ", cyberpi.get_firmware_version))
lines.append(ask("name     ", cyberpi.get_name))

# Read the shield three times - an intermittent answer means a loose
# connector, a consistent one means the firmware genuinely isn't seeing it.
reads = []
for _ in range(3):
    try:
        reads.append(cyberpi.get_shield())
    except Exception as e:
        reads.append(type(e).__name__)
    time.sleep(0.3)
lines.append(f"shield x3: {reads}")

lines.append(ask("chassis V", cyberpi.get_extra_battery))
lines.append(ask("cyberpi V", cyberpi.get_battery))
lines.append(ask("eyes cm  ", lambda: cyberpi.ultrasonic2.get(1)))
lines.append(ask("floor    ", lambda: cyberpi.quad_rgb_sensor.get_gray(1, 1)))

# The decisive test: command a motor, then ask the encoder whether the
# wheel actually turned. The encoder counts real rotation, so it cannot be
# fooled by a command that was accepted and quietly ignored.
before = None
try:
    before = m.EM_get_angle("EM1")
except Exception as e:
    lines.append(f"encoder  : unreadable ({type(e).__name__})")

if before is not None:
    try:
        m.EM_set_power(60, "all")
        time.sleep(1.2)
        m.EM_stop("all")
    except Exception as e:
        lines.append(f"drive    : refused ({type(e).__name__})")
    try:
        after = m.EM_get_angle("EM1")
        moved = "WHEEL TURNED" if after != before else "wheel did not move"
        lines.append(f"encoder  : {before} -> {after}   {moved}")
    except Exception as e:
        lines.append(f"encoder  : unreadable after ({type(e).__name__})")

print("\n".join(lines))
print("\nPaste these lines back - that's all I need.")
