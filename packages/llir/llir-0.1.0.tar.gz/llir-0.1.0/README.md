LLIR
====

[![PyPI version](https://badge.fury.io/py/llir.svg)](https://badge.fury.io/py/llir)
[![Python](https://img.shields.io/pypi/pyversions/llir)](https://badge.fury.io/py/llir)

Low level input recorder or LLIR is a Python package for
recording low level mouse and keyboard events and replaying
them back.

Why? Have you ever wondered why packages like `pyautogui` or
`pynput` or even programs like `AutoHotKey` don't work with
games? They either can't send input to games altogether or the
mouse input "works" but it's completely broken.

Well, I created this package to address these issues. 
Using low level (hence the name) methods and APIs to
record and playback the input, it works with a [lot of games](#notes)
and also in normal application.


Table of Content
----------------
<!-- TOC -->
* [LLIR](#llir)
  * [Table of Content](#table-of-content)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Start recording](#start-recording)
    * [Stop recording](#stop-recording)
    * [Start replaying](#start-replaying)
      * [To start replaying a macro that was recorded during this run](#to-start-replaying-a-macro-that-was-recorded-during-this-run)
      * [To start replaying a macro that was saved to a file](#to-start-replaying-a-macro-that-was-saved-to-a-file)
    * [Stop replaying](#stop-replaying)
    * [Stop listening](#stop-listening)
    * [Changing the default shortcuts](#changing-the-default-shortcuts)
    * [Keeping old macros](#keeping-old-macros)
  * [Notes](#notes)
  * [Limitations](#limitations)
  * [How it works](#how-it-works)
  * [What this package isn't](#what-this-package-isnt)
  * [License](#license)
<!-- TOC -->


Installation
------------
This package supports Python >= 3.10, and it has been tested
on Windows 10 and 11, though it should work on Windows 7+.

To install simply run:
```
pip install llir
```

If you can't use Python 3.10+, you can modify the syntax
for the type hints or use 
`from future import __anotations__`
and change any type imports that don't exist in the `typing`
package to `typing_extensions`.


Usage
-----
The main entry point to the package is the 
`LowLevelInputRecorder` class.
import as the following:
```python
from llir import LowLevelInputRecorder
```

There are two ways to use it, programmatically or using
shortcuts. in either case, you must first call 
`start_listening`:
```python
recorder = LowLevelInputRecorder()
recorder.start_listening()
```

Now the class is ready to accept actions.\
If wish to control the actions using shortcuts,
these are all the lines of code you need to run.

### Start recording
To start recording mouse and keyboard input so you can
replay them back later, call `start_recording` or press
the shortcut for starting recording as specified in
`start_recording_shortcut` which can be defined at class
creation. The default shortcut is `left ctrl + left arrow`.

**Note**: You can only start recording if `start_listening`
has been called and the class isn't replaying a macro.

### Stop recording
Call `stop_recording` or the press the 
`start_recording_shortcut` (default is 
`left ctrl + right arrow`).
This method can be called at any time, it will call the
correct thing only the class is currently recording.

### Start replaying
#### To start replaying a macro that was recorded during this run
Call `start_replaying` or press the `start_replaying_shortcut`
(default is `left ctrl + down arrow`).

**Note**: You can only start replaying a macro if the class
isn't currently recording input and `start_listening` has
been called.

#### To start replaying a macro that was saved to a file
If you haven't recorded any input yet, you can replay an
already recorded macro that was saved to a file by specifying the
file path where the macro was saved to at class 
initialization, for example:
```python
recorder = LowLevelInputRecorder(save_file_path="path/to/file")
recorder.start_listening()
recorder.start_replaying()
```

### Stop replaying
Call `stop_replaying` or press the `stop_replaying_shortcut`
(default is `left ctrl + up arrow`).

### Stop listening
To stop listening for input and effectively shutdown the class,
call `stop_listening` or press the `stop_shortcut` (default
is `left ctrl + left shift + x`).

**Note**: You can't perform any other actions after
this method is called.
To start the class again so you can record/replay input,
`start_listening` must be called again.

### Changing the default shortcuts
To change the default shortcuts, pass the `ScanCode`s for
the keys you want to be pressed to trigger as specific
action to the class initializer seperated by a plus sign.

For example, to set the shortcut for starting recording
to left shift and the letter x:
```python
recorder = LowLevelInputRecorder(start_recording_shortcut="0x002A+0x002D")
```
Where "0x002A" is the ScanCode for the left shift key and
0x002D is the ScanCode for the letter "X".

A list of scan codes can be found at the official 
[Microsoft documentation](https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input#scan-codes).

### Keeping old macros
The default behaviour is discarding any previously
recorded input when `start_recording` is called.\
If you wish to keep any old macros that were recorded,
set `append_new_input` to True when initializing the class.


Notes
-----
1. To record keyboard and mouse events and be able to replay them on a different window (application), the python
   process that ran the script must be on the same level of privilege as that application,
   with some notable exceptions.
   So for example, if you run a game as an administrator, you must also run Python (through your IDE or CMD) as an
   administrator to be able to record keyboard and mouse inputs and replay them in that window.
   A notable exception to this is Task Manager, even if you launch it normally, you need admin privileges to
   "send input" to it.
2. The only blocking function in this class is `start_replaying` for replaying back the input, the other functions
   return immediately, so you will need to place `time.sleep()` calls for example after starting to record.
3. You can't use the class after you called `stop_listening` unless you call `start_listening()` again.
4. Some games block the `SendInput` API which this packages uses under the
   hood to replay back the recorded input. These games are usually online games that
   do this to protect against hacking, usage of this package with such
   games will not work and might get you banned.


Limitations
-----------
1. **Touchpads**: 
    1. Windows treats touchpads differently than mouses,
      so touchpad specific functionality aside than basic functionality
      isn't supported, like gestures (3 finger touch for example).
    2. Moving, left and right clicks always work.
    3. However, scrolling only works
      correctly if it's recorded, but sometimes, depending on the application, it's
      not recorded, as if the application had "swallowed" it.
      It works correctly in Pycharm and Minecraft but not in Firefox for example.
2. **Windows UI shortcuts**: Shortcuts like `alt-tapping` to switch windows
   or `Windows + D` to show the desktop don't work.


How it works
------------
There are different ways to listen for keyboard, mouse and
other hardware devices input in Windows, such as [LowLevelMouseProc ](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/legacy/ms644986(v=vs.85)) callback.\
The problem with most "user-mode" methods is that they
either can't record input happening in other applications
or they don't record input at a low enough level.\
Not recording at a "low enough level" has some caveats,
one of which is that the mouse input will be altered
by the operating system, like applying acceleration and
custom scroll distance and threshold.

The other possible solution might then be to create a custom
driver or an interceptor, but that's too much work and Python
isn't really the language for doing that.\

Well, there's one last method we haven't discussed yet, the
[Raw Input API](https://learn.microsoft.com/en-us/windows/win32/inputdev/about-raw-input).\
The Raw Input API can be used to get low level device input
(like a mouse, touchpad or keyboard) before they are
processed by the operating system.\
Also, a lot of games, especially newer ones use this API to
get device input.

Why care about getting "low level" mouse and keyboard input?\
Most games work correctly regardless of keyboard layout/language
(a modification done by the Operating System). Additionally most
games lock the cursor to the middle of the screen, rendering
methods such as recording and setting the cursor position useless.\
Recording low level input events allows us to obtain [scan codes](https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input#scan-codes)
and [mouse movement deltas](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-rawmouse),
which then can be sent to games in the same format they understand.

This packages creates a window that's invisible and registers
raw mouse and keyboard input devices to it as input sinks,
meaning that we get input events even if other programs
are in the foreground (focused)¹.\
Then the recorded raw input is played back using the [SendInput](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput)
API.

If you still want to know more about the inner workings
of this, check the function documentation and comments in
`raw_input.py` and `send_input.py`, they contain
some useful information and gotchas when working with these APIs.

One last thing that this package does is special handling when replaying
back the input, it tries to the best it can to replay the recorded
events in exactly the same time they were recorded in.\
In other words, if the time difference between the first event and
second event is 500 ms, it will attempt to execute the second
event at exactly 500 ms after the first event.\
Why is this important? Well for general automation and normal applications
it's not an issue for there to be extra delay between the recorded events
times and the execution time.\
However, in games this is most likely an issue. Hopefully an example would
make this more clear: Suppose the recorded macro was moving the mouse to
the right by 5 pixels (remember? mouse deltas) every 100 ms for 5 seconds, 
given the same starting position, on the desktop it doesn't matter if
replaying back the macro took 10 seconds and the delay between each
input was 200 ms, the cursor will end up at the same location as the one
when the macro was recorded.\
But in a game, the player's camera will be pointing at a different
location than the one were it ended pointing at when recording the macro
due to game mechanics, how it handles input and acceleration and movement
delta threshold settings.\
The variable execution "lag" effect will be more troublesome the longer the
macro is, playing back a 1-second macro might take 1.05 seconds which might 
not be a problem, but playing back a 100-second macro might take 120 seconds,
which will most likely be a problem.\
To mitigate this, a hybrid approach of short sleeps and busy-waiting to 
achieve timing accuracy used. This is more heavy on the CPU than simply
using `time.sleep(time_difference_between_this_event_and_previous_event)`,
but it's not that much (2% CPU usage on an old 6 core Ryzen 2600 processor) but is much 
more accurate.\
A better algorithm for achieving this "real-time" constraint probably exists,
nonetheless I couldn't find any useful information on this topic.

<sup>¹ This is subject to program privilege, check the [notes](#notes) for more information.</sup>


What this package isn't
-----------------------
This package is not intended as a replacement for other Python packages
such as `pynput`, `pyautogui`, `keyboard` or dedicated automation
programs like `AutoHotKey`.\
These solutions offer the functionality to programmatically define
mouse and keyboard (and much more) actions and then execute them using a user-friendly
interface.\
This package is only intended for recording and replaying **_raw_** mouse
and keyboard inputs, even though you can use it as the packages
mentioned above, it's not as easy or convenient to do so.


License
-------
This project is licensed under the [MIT license](https://github.com/Yazan-Sharaya/llir/blob/main/LICENSE).
