"""Define constants for use/to check the result of calls to the Windows API."""

# Constants for SendInput.
INPUT_MOUSE = 0x0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_WHEEL = 0x0800
INPUT_KEYBOARD = 0x1
KEYEVENTF_KEYUP = 0x0002  # We only need to define keyup, because the SendInput function assumes keydown otherwise.
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_EXTENDEDKEY = 0x0001

# Constants for raw input.
# Set to enable the caller to receive the input even when the caller is not in the foreground.
RIDEV_INPUTSINK = 0x00000100
RID_INPUT = 0x10000003
WM_INPUT = 0x00FF  # Mouse input event.
HID_USAGE_PAGE_GENERIC = 0x01
HID_USAGE_GENERIC_MOUSE = 0x02
HID_USAGE_GENERIC_KEYBOARD = 0x06
RIM_TYPEMOUSE = 0x0  # Device type of WM_INPUT
RIM_TYPEKEYBOARD = 0x1
MAPVK_VK_TO_VSC_EX = 4
RI_KEY_E0 = 2
