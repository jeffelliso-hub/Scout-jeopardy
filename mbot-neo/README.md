# Blip

An mBot Neo (Makeblock CyberPi + mBot2 chassis) programmed from scratch in
MicroPython, with no Makeblock software anywhere in the loop.

Working name is **Blip**. The intent is that the kid names him on first boot
and he remembers it forever.
and he remembers it forever.

## The idea

Most AI robot projects put the brain in the cloud. The robot becomes a puppet:
dead when the Wi-Fi drops, and starting from zero every single conversation.

Here the relationship is inverted. **The cloud does not control him. It teaches
him.**

He has a *self* that lives on the board and survives power cycles - mood,
energy, curiosity, boredom, who he's met, and a growing library of tricks he's
been taught. Every cloud interaction ends by writing something durable into
that local brain. He accumulates. The robot in November knows things he didn't
in September, and knows them with the router unplugged.

## Layers

| Layer | Needs network? | What it is |
|---|---|---|
| **Body** | no | Motion, screen, lights, sound - as expressive primitives (`nod`, `sulk`, `startle`, `approach`), not raw motor calls |
| **Self** | no | Persistent mood and memory on the board's filesystem. The reason he's a pet and not a program |
| **Instincts** | no | The always-on loop. Reacts to approach, being picked up, lights out, loud noises, the edge of the table. Gets bored. Seeks attention |
| **Tricks** | no | Learned behaviours, stored as *data* in a small interpreted format. Taught once, his forever |
| **Games** | no | Hide and seek, freeze dance, red-light-green-light. He *proposes* these when bored and someone's nearby |
| **Imagination** | yes | Speech in, a mind, and a reply expressed as body language - plus the ability to author new tricks |

Everything above the last row works on a dead network. That's the whole point.

## Two design decisions worth defending

**He does not speak English.** Text-to-speech costs a cloud round-trip on every
utterance and dies offline. Instead he has an expressive beep-language - pitch
and rhythm carrying emotion - with words on his screen. Instant, offline,
far more charming, and kids learn to read a character's tone. The cloud still
understands *them* perfectly; he just answers in his own voice.

**Tricks are data, never generated code.** A trick is a small interpreted
structure, never `exec()` on model output. He cannot be bricked by something he
was taught, and a trick can be inspected, edited, and shown to the kid as a
thing they made.

## Teaching him

> "When I clap twice, spin around and beep like you're mad."

That goes out once. What comes back is not an action - it's a trick, written
into his filesystem, interpreted locally from then on. The kid programmed a
robot by talking to it, and it still works next week with the internet off.

## Ambient listening

He listens continuously by choice. So: the screen and the LED ring make it
*visible* when he's paying attention, and there's a hard mute. A kid should be
able to see when a machine is listening to them.

## Status

Step 1 - reconnaissance. `tools/probe.py` reports what the board actually
exposes over USB serial. It is read-only, and never touches firmware.

```
pip install pyserial
python3 tools/probe.py
```

Nothing else here is built yet. The probe results decide the rest.

## Decisions

- Makeblock's `cyberpi` Python package is fair game as a dependency. The thing
  being avoided is the *app*, not their code.
- Firmware is Makeblock's own ESP-IDF build (v44.01.009, Jan 2022) on an
  ESP32. There is no MicroPython REPL on the UART; the way in is their serial
  protocol. `tools/probe2.py` established this from the boot banner.
- Opening the serial port reboots him - DTR/RTS are wired to the reset line.
  Harmless, and it means a boot banner is available on demand.
- Opening the USB serial port with DTR/RTS asserted pins the ESP32 in reset:
  the backlight stays on, the screen goes blank, and no menu appears. Recovery
  is unplug USB, power cycle. Every tool here releases both lines on open,
  including underneath Makeblock's library, which opens the port itself.

## What the hardware actually gives us

Confirmed against firmware 44.01.009 by round trip, not by documentation:

- **Wheels** are `cyberpi.mbot2`: forward, backward, turn_left, turn_right,
  straight, drive_power, plus encoder calls (`EM_get_angle`, `EM_get_speed`)
  that read back real wheel movement. He can know how far he has gone.
- **Eyes** are `cyberpi.ultrasonic2`; the floor sensor is
  `cyberpi.quad_rgb_sensor` with line, colour and grey-level reads.
- **Balance and handling**: is_shake, is_freefall, is_faceup, is_tiltleft,
  get_roll/pitch/yaw. Enough to know when he has been picked up.
- **Microphone** records on-board: `audio.record`, `stop_record`,
  `play_record`.
- **His speech endpoints are settable**: `set_recognition_url`,
  `recognition_set_url`, `tts_set_url`, `translate_set_url`. He can listen
  with his own microphone and send the audio to a server we run, which is the
  whole conversation layer without Makeblock's cloud in the path.
- `goto_offline_mode` exists alongside the online handshake, which is the
  thread to pull for running standalone.
