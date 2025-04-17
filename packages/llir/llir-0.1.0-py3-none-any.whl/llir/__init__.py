"""
LLIR or LowLevelInputRecorder can record and playback low level mouse and keyboard input using the
`RawInput` and `SendInput` APIs.

The main benefit of this package is usage in games or game-like applications, as they often use the `RawInput` API
to get unfiltered input events.

This package is not intended as a replacement for other popular packages or programs like `pyautogui`, `pynput` or
`AutoHotKey` because they offer more extensible and general purpose macro creation and automation.
Rather, this package was created because these offerings are not good (if not impossible) to use in video games due
to how games process user input.

For more information about how it works and usage, check `LowLevelInputRecorder` class documentation and `README.md`.

Notes
-----
This package only works on Windows because it uses Windows only APIs like `GetRawInput` and `SendInput`.
"""
import sys

if sys.platform != "win32":
    raise OSError("llir can only run on Windows because it depends on Windows specific APIs.")

from llir.recorder import LowLevelInputRecorder

__version__ = "0.1.0"
