"""Defines all the `structs` that will be used by the Windows API using `ctypes`."""
import ctypes.wintypes as wintypes
import ctypes


# Missing from ctypes.wintypes
LRESULT = ctypes.c_long
HCURSOR = ctypes.c_void_p


# =========================== #
# Structures for GetCursorPos #
# =========================== #

class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long)
    ]


# ======================== #
# Structures for SendInput #
# ======================== #

# Define the MOUSEINPUT structure, see https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.PULONG),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVK", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.PULONG),
    ]


# Define the INPUT union
class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
    ]


# Define the INPUT structure, see https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
class INPUT(ctypes.Structure):
    # See https://docs.python.org/3/library/ctypes.html#ctypes.Structure._anonymous_ for why `_anonymous_` is useful.
    _anonymous_ = ("union",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUTUNION),
    ]


# ======================================== #
# Structures for capturing raw mouse input #
# ======================================== #

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawinputdevice
class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", ctypes.c_ushort),
        ("usUsage", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("hwndTarget", ctypes.c_void_p)
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawinputheader
class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", ctypes.c_ulong),
        ("dwSize", ctypes.c_ulong),
        ("hDevice", ctypes.c_void_p),
        ("wParam", ctypes.c_ulong)
    ]


class _ButtonData(ctypes.Structure):
    _fields_ = [
        ("usButtonFlags", ctypes.c_ushort),
        ("usButtonData", ctypes.c_ushort)
    ]


class _ButtonsUnion(ctypes.Union):
    _anonymous_ = ("DUMMYSTRUCTNAME",)
    _fields_ = [
        ("ulButtons", ctypes.c_ulong),
        ("DUMMYSTRUCTNAME", _ButtonData)
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawmouse
class RAWMOUSE(ctypes.Structure):
    _anonymous_ = ("DUMMYUNIONNAME",)
    _fields_ = [
        ("usFlags", ctypes.c_ushort),
        ("DUMMYUNIONNAME", _ButtonsUnion),
        ("ulRawButtons", ctypes.c_ulong),
        ("lLastX", ctypes.c_long),
        ("lLastY", ctypes.c_long),
        ("ulExtraInformation", ctypes.c_ulong)
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawkeyboard
class RAWKEYBOARD(ctypes.Structure):
    _fields_ = [
        ("MakeCode", ctypes.c_ushort),
        ("Flags", ctypes.c_ushort),
        ("Reserved", ctypes.c_ushort),
        ("VKey", ctypes.c_ushort),
        ("Message", ctypes.c_uint),
        ("ExtraInformation", ctypes.c_ulong),
    ]


class RAWINPUT_DATA_UNION(ctypes.Union):  # noqa
    _fields_ = [
        ("mouse", RAWMOUSE),
        ("keyboard", RAWKEYBOARD),
    ]


# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawinput
class RAWINPUT(ctypes.Structure):
    _anonymous_ = ("data",)
    _fields_ = [
        ("header", RAWINPUTHEADER),
        ("data", RAWINPUT_DATA_UNION)
    ]


# Create a message loop to handle WM_INPUT messages
class WNDCLASS(ctypes.Structure):
    _fields_ = [("style", ctypes.c_uint),
                ("lpfnWndProc",
                 ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)),
                ("cbClsExtra", wintypes.UINT),
                ("cbWndExtra", wintypes.UINT),
                ("hInstance", wintypes.HINSTANCE),
                ("hIcon", wintypes.HICON),
                ("hCursor", HCURSOR),
                ("hbrBackground", wintypes.HBRUSH),
                ("lpszMenuName", wintypes.LPCWSTR),
                ("lpszClassName", wintypes.LPCWSTR)]
