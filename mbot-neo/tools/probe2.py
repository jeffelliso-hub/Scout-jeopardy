#!/usr/bin/env python3
"""
probe2.py - find out what the CyberPi's serial port is actually saying.

probe1 found the CH340 bridge (1a86:7523) but got zero bytes back. That means
one of: the board is off, we guessed the baud rate wrong, or opening the port
yanked the reset line and held him down.

This tries all three. Everything here is read-mostly and reversible; nothing
is written to his filesystem and firmware is never touched.

    python3 probe2.py                 # sweep baud rates, listen, nudge
    python3 probe2.py --listen 30     # pure eavesdrop - press his buttons
    python3 probe2.py --reset         # pulse RTS to catch a boot banner
"""

import argparse
import sys
import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    sys.exit("pip install pyserial")

# Fastest to slowest by likelihood for this class of board.
BAUDS = [115200, 921600, 460800, 230400, 57600, 9600, 38400, 74880]
CH340 = (0x1A86, 0x7523)


def find_port(explicit=None):
    if explicit:
        return explicit
    ports = list(list_ports.comports())
    for p in ports:                                  # exact CH340 match wins
        if (p.vid, p.pid) == CH340:
            return p.device
    for p in ports:                                  # else any usbserial
        if "usbserial" in p.device or "ttyUSB" in p.device:
            return p.device
    return None


def open_quiet(port, baud, timeout=0.2):
    """Open WITHOUT asserting DTR/RTS, so we don't hold the board in reset."""
    s = serial.Serial()
    s.port = port
    s.baudrate = baud
    s.timeout = timeout
    try:
        s.dtr = False
        s.rts = False
    except Exception:
        pass          # not every driver lets you preset these; press on
    s.open()
    try:
        s.dtr = False
        s.rts = False
    except Exception:
        pass
    return s


def drain(ser, seconds):
    buf = b""
    end = time.time() + seconds
    while time.time() < end:
        chunk = ser.read(ser.in_waiting or 1)
        if chunk:
            buf += chunk
        else:
            time.sleep(0.02)
    return buf


def describe(raw):
    """Say something useful about a pile of bytes."""
    if not raw:
        return "silence"
    printable = sum(1 for b in raw if 32 <= b < 127 or b in (10, 13, 9))
    ratio = printable / len(raw)
    text = raw.decode("utf-8", errors="replace")
    kind = "TEXT" if ratio > 0.8 else ("BINARY" if ratio < 0.4 else "mixed")
    return f"{len(raw)} bytes, {kind}\n      repr: {raw[:220]!r}\n      text: {text[:220]!r}"


def sweep(port, settle):
    print(f"\nSweeping baud rates on {port}")
    print("(passively listening, then poking with newline + Ctrl-C)\n")
    hits = []
    for baud in BAUDS:
        try:
            ser = open_quiet(port, baud)
        except Exception as e:
            print(f"  {baud:>7} : cannot open - {e}")
            continue
        try:
            time.sleep(settle)
            passive = drain(ser, 1.2)

            ser.reset_input_buffer()
            ser.write(b"\r\n")
            time.sleep(0.3)
            nl = drain(ser, 0.6)

            ser.reset_input_buffer()
            ser.write(b"\r\x03\x03")          # interrupt anything running
            time.sleep(0.3)
            ctrlc = drain(ser, 0.8)

            ser.reset_input_buffer()
            ser.write(b"\r\x01")              # ask for a raw REPL
            time.sleep(0.3)
            rawrepl = drain(ser, 0.8)
        finally:
            ser.close()

        got = passive + nl + ctrlc + rawrepl
        if got:
            hits.append(baud)
            print(f"  {baud:>7} : ANSWERED")
            for label, blob in (("idle", passive), ("newline", nl),
                                ("ctrl-c", ctrlc), ("ctrl-a", rawrepl)):
                if blob:
                    print(f"      [{label}] {describe(blob)}")
            if b"raw REPL" in got:
                print("      *** MicroPython raw REPL. This is the jackpot. ***")
            elif b">>>" in got:
                print("      *** A REPL prompt. Very promising. ***")
        else:
            print(f"  {baud:>7} : silence")
    return hits


def reset_and_capture(port):
    """Pulse RTS to reboot the board and catch whatever it prints on boot.

    RTS alone is a plain reset. DTR is deliberately left high so we never
    drop him into the ROM download mode.
    """
    print("\nPulsing RTS to reset him, then listening for a boot banner.")
    print("(A reset is harmless and reversible - nothing is written.)\n")
    for baud in (115200, 74880, 921600, 9600):
        try:
            ser = open_quiet(port, baud)
        except Exception as e:
            print(f"  {baud:>7} : cannot open - {e}")
            continue
        try:
            ser.dtr = False
            ser.rts = True          # hold in reset
            time.sleep(0.15)
            ser.rts = False         # release - he boots
            boot = drain(ser, 3.0)
        finally:
            ser.close()
        print(f"  {baud:>7} : {describe(boot)}")


def eavesdrop(port, seconds):
    print(f"\nListening on {port} at 115200 for {seconds}s.")
    print("Press his buttons, waggle the joystick, roll him around.")
    print("If ANY bytes appear, the link is alive and we just need the protocol.\n")
    ser = open_quiet(port, 115200, timeout=0.2)
    try:
        raw = drain(ser, seconds)
    finally:
        ser.close()
    print(f"  {describe(raw)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port")
    ap.add_argument("--listen", type=int, metavar="SECONDS")
    ap.add_argument("--reset", action="store_true")
    ap.add_argument("--settle", type=float, default=0.4)
    args = ap.parse_args()

    port = find_port(args.port)
    if not port:
        sys.exit("No CH340 / usbserial port found. Is he plugged in?")
    print(f"Target: {port}")

    if args.listen:
        eavesdrop(port, args.listen)
    elif args.reset:
        reset_and_capture(port)
    else:
        hits = sweep(port, args.settle)
        print()
        if hits:
            print(f"He answered at: {hits}")
        else:
            print("Silent at every baud rate.")
            print("Next: confirm his power switch is ON with lights/screen showing,")
            print("then re-run. After that, try:  python3 probe2.py --reset")


if __name__ == "__main__":
    main()
