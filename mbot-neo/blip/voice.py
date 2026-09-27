"""
voice.py - Blip doesn't speak English. He beeps, and the beeps mean something.

Text-to-speech would cost a network round trip per utterance and go mute the
moment the wifi drops. Pitch and rhythm cost nothing, work on a dead network,
and a kid reads tone far faster than they read words.

The grammar is deliberately small, so it stays learnable:

    rising    -> curious, asking, hopeful
    falling   -> disappointed, sleepy, no
    fast      -> excited, urgent
    slow      -> tired, sulking, thinking
    low       -> grumpy, serious
    high      -> delighted, surprised
    repeated  -> insistent - he wants something

Every phrase pairs with a face, because a beep alone is ambiguous and a beep
with a face is a character.
"""

# Equal temperament from A4, rounded - close enough for a piezo speaker.
NOTES = {
    "C4": 262, "D4": 294, "E4": 330, "F4": 349, "G4": 392, "A4": 440, "B4": 494,
    "C5": 523, "D5": 587, "E5": 659, "F5": 698, "G5": 784, "A5": 880, "B5": 988,
    "C6": 1047, "E6": 1319, "G6": 1568,
}

# name -> (notes, seconds per note, face)
PHRASES = {
    # -- greeting and attention -------------------------------------------
    "hello":      (["C5", "E5", "G5"],              0.12, "^   ^"),
    "hey":        (["G5", "C6"],                    0.10, "o   o"),
    "goodbye":    (["G5", "E5", "C5"],              0.16, "-   -"),

    # -- asking ------------------------------------------------------------
    "curious":    (["E5", "G5"],                    0.11, "o   O"),
    "question":   (["C5", "E5", "G5", "C6"],        0.09, "?   ?"),
    "listening":  (["A5"],                          0.08, "O   O"),

    # -- pleased -----------------------------------------------------------
    "happy":      (["C5", "E5", "G5", "C6", "G5"],  0.08, "^   ^"),
    "delighted":  (["G5", "C6", "E6", "G6"],        0.06, "*   *"),
    "proud":      (["C5", "G5", "C6"],              0.14, "^   ^"),

    # -- displeased --------------------------------------------------------
    "grumpy":     (["E4", "D4", "C4"],              0.18, ">   <"),
    "no":         (["G4", "C4"],                    0.20, "-   -"),
    "startled":   (["C6", "G5", "C6", "G5"],        0.05, "O   O"),
    "hurt":       (["E5", "C5", "A4", "F4"],        0.15, "v   v"),

    # -- inner life --------------------------------------------------------
    "bored":      (["C5", "B4", "A4", "G4"],        0.22, "-   -"),
    "thinking":   (["E5", "E5", "E5"],              0.20, ".   ."),
    "sleepy":     (["G4", "F4", "E4", "D4", "C4"],  0.28, "_   _"),
    "waking":     (["C4", "E4", "G4", "C5"],        0.18, "o   o"),

    # -- insisting ---------------------------------------------------------
    "nudge":      (["A5", "A5"],                    0.09, "^   ^"),
    "pester":     (["A5", "A5", "A5", "A5"],        0.07, "O   O"),
}


def say(body, phrase, show_face=True):
    """Speak one phrase. Unknown names fall back to a neutral chirp."""
    notes, beat, face = PHRASES.get(phrase, (["E5"], 0.12, "o   o"))
    if show_face:
        body.face(face)
    for note in notes:
        body.tone(NOTES.get(note, 660), beat)
    return face


def chirp(body, hz=660, seconds=0.08):
    """A single unstyled blip - punctuation rather than a word."""
    body.tone(hz, seconds)


def vocabulary():
    return sorted(PHRASES)
