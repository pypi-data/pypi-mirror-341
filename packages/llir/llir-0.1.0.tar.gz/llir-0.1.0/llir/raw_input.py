"""
Module that contains function for setting up capturing input using the Raw Input API.
Getting the input events for the keyboard and mouse is done though callbacks, call `register_callback` to register a
callback for the input device you want.
"""
from typing import Callable, Literal, overload, cast, TypeAlias
from ctypes import wintypes
import ctypes
import threading

from llir.structs import WNDCLASS, RAWINPUTDEVICE, RAWINPUTHEADER, RAWINPUT
from llir.constants import (
    RID_INPUT,
    RIM_TYPEMOUSE,
    RIM_TYPEKEYBOARD,
    WM_INPUT,
    RIDEV_INPUTSINK,
    HID_USAGE_PAGE_GENERIC,
    HID_USAGE_GENERIC_MOUSE,
    HID_USAGE_GENERIC_KEYBOARD,
    MAPVK_VK_TO_VSC_EX,
)


MouseCallback: TypeAlias = Callable[[int, int, int, int, int], None]
KeyboardCallback: TypeAlias = Callable[[int, int, int, int], None]

user32 = ctypes.windll.user32

_should_quit = threading.Event()
_has_quit = threading.Event()
_created_hwnd = 0
_mouse_callbacks: list[MouseCallback] = []
_keyboard_callbacks: list[KeyboardCallback] = []

DefWindowProcW = user32.DefWindowProcW
DefWindowProcW.argtypes = wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
DefWindowProcW.restype = ctypes.c_long


@overload
def register_callback(callback_for: Literal["mouse"], callback: MouseCallback) -> None: ...


@overload
def register_callback(callback_for: Literal["keyboard"], callback: KeyboardCallback) -> None: ...


def register_callback(callback_for: Literal["mouse", "keyboard"], callback: MouseCallback | KeyboardCallback) -> None:
    """
    Register a callback that will be called when `callback_for` event occurs.

    Mouse callbacks should take five arguments: buttonFlags, lastX, lastY, scroll direction and ulExtraInformation [1]_.
    Keyboard callbacks should take four arguments: key state (flags), scan code, vkey and ExtraInformation [2]_.

    Check the docs linked in the References section to learn more about what each value mean.

    Raises
    ------
    ValueError
        If `callback_for` is not "mouse" or "keyboard".

    Notes
    -----
    (ul)ExtraInformation is device specific and I couldn't find any documentation of what the values
    I was getting mean, I just know that they are big numbers and that they will be zero if the event was triggered
    by a user action (e.g. moving the mouse, pressing a key) and that they will contain a positive integer if the
    event generated "synthetically", e.g. using the `SendInput` API.

    References
    ----------
    .. [1] https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawmouse
    .. [2] https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawkeyboard
    """
    if callback_for == "mouse":
        _mouse_callbacks.append(cast(Callable[[int, int, int, int, int], None], callback))
    elif callback_for == "keyboard":
        _keyboard_callbacks.append(cast(Callable[[int, int, int, int], None], callback))
    else:
        raise ValueError(f"Unsupported callback type: {callback_for}. Only 'mouse' and 'keyboard' are allowed.")


def _raw_input_window_procedure(hwnd, msg, wparam, lparam):
    """
    The function that Windows will pass messages from the `Message Queue` to processing.

    This function only performs special processing if the `msg` type is WM_INPUT
    because it's only concerned with input devices.

    If the `msg` is WM_INPUT, mouse and keyboard raw input data are recorded,
    the `msg` is passed to the Default Window Procedure [1]_ to provide default processing otherwise.

    To see which data is recorded and how it's stored check the class docstring.

    `GetRawInputData` [2]_ function is used to get the raw input directly from the mouse and keyboard,
    before the OS performs any processing on it like acceleration.

    The name of the parameters passed to the function are the same as their C++ counterpart,
    except they are in lowercase.

    Callbacks
    ---------
    You can register callbacks for when a mouse or a keyboard event happens using the `register_callback` function.

    For mouse events, the button flags, lastx, lasty, scroll direction and ulExtraInformation are passed are based
    to the callback.
    For keyboard events, the key flags, make code (scan code), virtual key code and ExtraInformation are passed
    to the callback.

    **Note** that (ul)ExtraInformation is device specific and I couldn't find any documentation of what the values
    I was getting mean, I just know that they are big numbers and that they will be zero if the event was triggered
    by a user action (e.g. moving the mouse, pressing a key) and that they will contain a positive integer if the
    event generated "synthetically", e.g. using the `SendInput` API.

    References
    ----------
    .. [1] https://learn.microsoft.com/en-us/windows/win32/winmsg/about-window-procedures
    .. [2] https://learn.microsoft.com/en-us/windows/win32/inputdev/about-raw-input
    """
    if msg == WM_INPUT:
        dw_size = wintypes.UINT(0)
        # First call: get required size
        user32.GetRawInputData(
            lparam, RID_INPUT, None, ctypes.byref(dw_size), ctypes.sizeof(RAWINPUTHEADER))

        lpb = ctypes.create_string_buffer(dw_size.value)

        # Second call: get actual data
        res = user32.GetRawInputData(
            lparam,
            RID_INPUT,
            lpb,
            ctypes.byref(dw_size),
            ctypes.sizeof(RAWINPUTHEADER))

        if res != dw_size.value:
            print("GetRawInputData did not return correct size")
            return 1

        # Cast buffer to RAWINPUT pointer
        rawinput_ptr = ctypes.cast(lpb, ctypes.POINTER(RAWINPUT))
        raw = rawinput_ptr.contents

        # Check type and access data
        if raw.header.dwType == RIM_TYPEMOUSE:
            # The usButtonData where the wheel movement is stored is a ushort and in the docs for the RAWINPUT
            # structure. A positive value indicates that the wheel was rotated forward and a negative
            # value indicates that the wheel was rotated backward.
            # So we need to cast the ushort to a short to get positive/negative values.
            mouse = raw.mouse
            scroll_direction = ctypes.c_short(mouse.usButtonData).value
            for callback in _mouse_callbacks:
                callback(
                    mouse.usButtonFlags, mouse.lLastX, mouse.lLastY, scroll_direction, mouse.ulExtraInformation)
        elif raw.header.dwType == RIM_TYPEKEYBOARD:
            # The following checks were taken from:
            # https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawkeyboard#remarks

            # Ignore key overrun state and keys not mapped to any virtual key code
            if raw.keyboard.MakeCode == 0xFF or raw.keyboard.VKey >= 0xFF:
                return 0

            if raw.keyboard.MakeCode:
                # Compose the full scan code value with its extended byte.
                # # Get the low byte (7 bits from MakeCode)
                # low_byte = raw.keyboard.MakeCode & 0x7f
                # # Determine the high byte based on flags
                # if raw.keyboard.Flags & RI_KEY_E0:
                #     high_byte = 0xe0
                # elif raw.keyboard.Flags & RI_KEY_E1:
                #     high_byte = 0xe1
                # else:
                #     high_byte = 0x00
                # # Combine low byte and high byte into scan_code
                # scan_code = low_byte | (high_byte << 8)

                # The Microsoft documentation says to do the above, I don't really know why and I haven't encountered
                # a benefit of doing yet in my testing. Of course if it wasn't hurting I wouldn't've commented it out,
                # because the scan_code is transformed, it makes it very hard later to detect shortcut key presses,
                # since the documented scan codes include the original `MakeCode` before the above modification, and
                # `SendInput` seems to work the same way for the transformed and the original one, so...
                scan_code = raw.keyboard.MakeCode
            else:
                # Scan code value may be empty for some buttons (for example multimedia buttons).
                # Try to get the scan code from the virtual key code.
                scan_code = user32.MapVirtualKeyA(raw.keyboard.VKey, MAPVK_VK_TO_VSC_EX)

            for callback in _keyboard_callbacks:
                callback(raw.keyboard.Flags, scan_code, raw.keyboard.VKey, raw.keyboard.ExtraInformation)

    return DefWindowProcW(hwnd, msg, wparam, lparam)


def create_window_and_start_processing(should_stop_callback: Callable[[], bool] | None = None) -> None:
    """
    Create a window that will be used for capturing raw mouse and keyboard input using the Windows message queue and
    start processing input device events.

    The created window isn't visible, as it's only used for capturing events because the only way to capture
    raw device input is by creating a window and assigning it a Window Procedure callback that checks for WM_INPUT
    events.

    The function for handling the messages (events) is `raw_input_window_procedure`.

    Parameters
    ----------
    should_stop_callback : callable, optional
        A function that will be called repeatedly every iteration of the message processing loop that decides if the
        processing should continue or terminate if it returns True.
        Note that this function is called every iteration of the loop it should be as fasta as possible to execute
        to not slow down message (like input events) processing.

    Notes
    -----
    This function will block indefinably or until `destroy_window_and_stop_processing` is called,
    so depending on the use case, it might be more desirable to start this function in a thread.
    """
    global _created_hwnd

    wndclass = WNDCLASS()
    wndclass.lpfnWndProc = ctypes.WINFUNCTYPE(
        ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)(_raw_input_window_procedure)
    wndclass.lpszClassName = "RawInputClass"
    user32.RegisterClassW(ctypes.byref(wndclass))

    hwnd = user32.CreateWindowExW(
        0, "RawInputClass", "Raw Input Window", 0, 0, 0, 0, 0, None, None, None, None)
    if not hwnd:
        raise ctypes.WinError()
    _created_hwnd = hwnd

    # Register raw mouse device
    rids = (RAWINPUTDEVICE * 2)()
    rids[0].usUsagePage = HID_USAGE_PAGE_GENERIC  # noqa
    rids[0].usUsage = HID_USAGE_GENERIC_MOUSE  # noqa
    rids[0].dwFlags = RIDEV_INPUTSINK  # noqa
    rids[0].hwndTarget = hwnd  # noqa

    # Register raw keyboard device
    rids[1].usUsagePage = HID_USAGE_PAGE_GENERIC  # noqa
    rids[1].usUsage = HID_USAGE_GENERIC_KEYBOARD  # noqa
    rids[1].dwFlags = RIDEV_INPUTSINK  # noqa
    rids[1].hwndTarget = hwnd  # noqa

    if not user32.RegisterRawInputDevices(ctypes.byref(rids), 2, ctypes.sizeof(rids[0])):
        raise ctypes.WinError(1, "Failed to register raw input devices.")

    msg = wintypes.MSG()
    # GetMessageW is blocking, so we can't exit until it receives a message.
    # PeekMessage is a workaround since it's none-blocking, however using it in Python isn't really feasible,
    # because Python is not fast enough to process/drop all the messages and the thread will hang.
    while user32.GetMessageW(ctypes.byref(msg), None, WM_INPUT, WM_INPUT) > 0:
        if (should_stop_callback and should_stop_callback()) or _should_quit.is_set():
            _has_quit.set()
            return
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))


def destroy_window_and_stop_processing() -> None:
    """
    Stop the message processing loop and destroy the created window.

    The call to this function will hang until a single mouse or keyboard input event is emitted because the message
    loop uses `GetMessageW` which is blocking if the Message Queue is empty and the check for the stopping criteria is
    inside the loop, meaning the check will not be reached until a message is inserted into the queue and `GetMessageW`
    gets it.
    """
    global _created_hwnd
    if not _created_hwnd:
        raise RuntimeError("No window is created yet. Call `create_window_and_start_processing` first.")
    _should_quit.set()
    _has_quit.wait()
    user32.DestroyWindow(_created_hwnd)
    user32.UnregisterClassW("RawInputClass", None)
    _created_hwnd = 0
    _should_quit.clear()
    _has_quit.clear()
