"""
Define four functions: `get_cursor_position`, `set_cursor_position`, `mouse_event` and `keyboard_event`
to send low level keyboard and mouse input using the `SendInput` API.
"""
from typing import Callable
import ctypes

from llir.structs import POINT, MOUSEINPUT, KEYBDINPUT, INPUT
from llir.constants import (
    INPUT_MOUSE,
    INPUT_KEYBOARD,
    MOUSEEVENTF_MOVE,
    MOUSEEVENTF_WHEEL,
    KEYEVENTF_KEYUP,
    KEYEVENTF_SCANCODE,
    KEYEVENTF_EXTENDEDKEY,
    RI_KEY_E0)

# Set the DPI awareness to on so get_cursor_position returns the correct coordinates.
try:
    # Windows 8+
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except AttributeError:
    # Windows Vista+
    ctypes.windll.user32.SetProcessDPIAware()


def _convert_raw_button_input_to_send_input(raw_input_button: int) -> int:
    """
    A mapping between `RawInput` API value for mouse button state and `SendInput` API.

    Raw mouse data is taken from https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawmouse
    Send input data is taken from https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
    """
    if not raw_input_button:  # Zero means the same for both APIs.
        return raw_input_button
    raw_input_to_mouseeventf = {
        0x0001: 0x0002,  # Left down
        0x0002: 0x0004,  # Left up
        0x0004: 0x0008,  # Right down
        0x0008: 0x0010,  # Right up
        0x0010: 0x0020,  # Middle down
        0x0020: 0x0040,  # Middle up
        0x0040: 0x0080,  # XBUTTON1 down
        0x0080: 0x0100,  # XBUTTON1 up
        0x0100: 0x0080,  # XBUTTON2 down (same as XBUTTON1 down in MOUSEEVENTF)
        0x0200: 0x0100,  # XBUTTON2 up (same as XBUTTON1 up in MOUSEEVENTF)
        0x0400: 0x0800,  # Wheel
        0x0800: 0x1000,  # HWheel
    }
    return raw_input_to_mouseeventf[raw_input_button]


def get_cursor_position() -> tuple[int, int]:
    """Get the current cursor position in x, y on the screen."""
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def set_cursor_position(x: int, y: int) -> None:
    """Set the cursor position"""
    ctypes.windll.user32.SetCursorPos(x, y)


def mouse_event(
        button: int,
        dx: int,
        dy: int,
        scroll_direction: int = 0,
        extra_info: int = 0,
        convert_from_raw: bool = True,
        callback: Callable[[int, int, int, int, int], None] | None = None) -> None:
    """
    Send a low level mouse move event using `SendInput` [1]_.

    Parameters
    ----------
    button : int
        Which mouse button to press or release [2]_.
        A full list for each button state (up or down, left or middle click) can be found in the `References`.
        Search for the `dwFlags` member to find the table with the values and what they mean.
    dx : int
        The relative movement vertically from the current cursor position, a positive integers means moving right
        and a negative value means moving to the left.
    dy: int
        The relative movement horizontally from the current cursor position, a positive integer means moving down
        and a negative value means moving up.
    scroll_direction : int, optional
        The scroll wheel direction and magnitude, zero means no scrolling, a positive integer means scrolling up
        and a negative integer means scrolling down.
        For magnitude, the value is usually +/- 120, which is typically scrolling up/down one line.
        Smaller values can be used for finer control like a touch bad or a free moving mouse scroll wheel,
        however, more events will need to be sent, because scrolling has a threshold, for example 5 scrolls that
        accumulate to 20 magnitude (arbitrary number) in 500 ms to scroll up or down one line.
    extra_info : int, optional
        An additional value associated with the mouse event. This can be some value that the application can
        call `GetMessageExtraInfo` to obtain this extra information.
    convert_from_raw : bool, optional
        Whether to convert the RawInput API recorded button data for the mouse buttons [3]_
        to be compatible with the `SendInput` API that this function uses. A table containing the values for
        raw mouse button input and what they mean can be found in the `References`, look for `usButtonFlags` member.
    callback : callable, optional
        A function to call with the same arguments of this function (button, dx, dy, scroll_direction, extra_info)
        when this function is called.
        Note that this callback is only called if `convert_from_raw` is set to True.

    References
    ----------
    .. [1] https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
    .. [2] https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
    .. [3] https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawmouse
    """
    mouse_data = [scroll_direction]
    if button and convert_from_raw:
        if callback:
            callback(button, dx, dy, scroll_direction, extra_info)
        # The `SendInput` api doesn't differentiate between which side button (typically called forward
        # and backward buttons, or 4 and 5) was clicked the same way it does for normal mouse clicks.
        # However, the `RawInput` api does, 0x0040 is 4th button down, 0x0080 is 4th button down, the same goes
        # for 0x0100 and 0x0200 and the 5th mouse button.
        # The way to define which mouse "X" button was clicked is by setting the correct XBUTTON1 or XBUTTON2 in
        # `mouseData, then the up and down action are mapped to the same value for both buttons.
        if button in (0x0040, 0x0080):  # XButton 4 up or down.
            mouse_data.append(0x0001)
        elif button in (0x0100, 0x0200):  # XButton 5 up or down.
            mouse_data.append(0x0002)
        button = _convert_raw_button_input_to_send_input(button)

    input_structure = INPUT()
    input_structure.type = INPUT_MOUSE
    # Loop because `mouseData` can only accept a single input either for scrolling or xinput.
    for curr_data in mouse_data:
        input_structure.mi = MOUSEINPUT(
            dx=dx,
            dy=dy,
            mouseData=curr_data,
            dwFlags=MOUSEEVENTF_MOVE | button | (MOUSEEVENTF_WHEEL if scroll_direction else 0),
            time=0,
            dwExtraInfo=ctypes.pointer(ctypes.c_ulong(extra_info)))
        ctypes.windll.user32.SendInput(1, ctypes.byref(input_structure), ctypes.sizeof(INPUT))


def keyboard_event(
        press: int,
        scan_code: int,
        vkey: int = 0,
        extra_info: int = 0,
        callback: Callable[[int, int, int, int], None] | None = None) -> None:
    """
    Send a low level keyboard event using `SendInput` [1]_

    Parameters
    ----------
    press : int
        Whether to press or release the key. 0 means press the key and 1 means release it. Even though it's more
        intuitive for 1 to mean press instead of release, it's kept this way to be consistent with the raw
        keyboard input data gathered by `GetRawInputData`. Note that for keys that don't have a scan code, like
        Volume Up, 2 means pressing the key and 3 means release it.
    scan_code : int
        The `ScanCode` [2]_ of the key to press. Scan codes are used because they show which keyboard key was
        pressed regardless of the current keyboard layout. This is useful because we can synthesize keystrokes that
        work regardless of the system state when the key was captured, which affects Virtual Keycodes and that's
        why they are not used. Additionally, most games use them because, for example, they want WASD to work no
        matter what keyboard layout is used.
    vkey : int
        The virtual-key code [3]_. Some keyboard inputs don't have `scan_code`, like Volume Up,
        in that case, pass 0 as the `scan_code` and pass this argument for the key you wish to press.
        A list of all virtual key codes can be found in the `References`.
    extra_info : int, optional
        An additional value associated with the keyboard event. This can be some value that the application can
        call `GetMessageExtraInfo` to obtain this extra information.
    callback : callable, optional
        A function to call with the same arguments of this function (press, scan_code, vkey, extra_info)
        when this function is called.

    Notes
    -----
    If press is set to 0 (press the key), the key will stay pressed until it's released by the user or the function
    is called again for the same key (scan code) with press set to 1 (release the key).

    References
    ----------
    .. [1] https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput
    .. [2] https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input#scan-codes
    .. [3] https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    """
    if not scan_code and not vkey:
        raise ValueError("One of `scan_code` or `vkey` must be set.")
    if callback:
        callback(press, scan_code, vkey, extra_info)
    # [1]:
    # When a key that has the E0 prefix is left up (unpressed), the raw input key flags will be
    # `RI_KEY_BREAK` (1) `or`ed with `RI_KEY_E0` (2) which will equal 3.
    # Send input doesn't have a flag that equals 3 for KEYBDINPUT struct, so if the key flags equal 3, it means that
    # the key is up so we set `KEYEVENTF_KEYUP` (SendInput API flag which equals 0x0002).
    # [2]:
    # Raw input sets the key flag to `RI_KEY_E0` (0x0002) if it has the extended E0 prefix.
    # Send input expects `KEYEVENTF_EXTENDEDKEY` (0x0001) to be set if the key has the E0 prefix.
    # The prefix is usually set on keys like multimedia.
    flags = ((KEYEVENTF_SCANCODE if scan_code else 0) |
             (KEYEVENTF_KEYUP if press in (1, 3) else 0) |  # [1]
             (KEYEVENTF_EXTENDEDKEY if press == RI_KEY_E0 else 0))  # [2]
    input_structure = INPUT()
    input_structure.type = INPUT_KEYBOARD
    input_structure.ki = KEYBDINPUT(
        wVK=vkey,
        wScan=scan_code,
        dwFlags=flags,
        time=0,
        dwExtraInfo=ctypes.pointer(ctypes.c_ulong(extra_info))
    )
    ctypes.windll.user32.SendInput(1, ctypes.byref(input_structure), ctypes.sizeof(INPUT))
