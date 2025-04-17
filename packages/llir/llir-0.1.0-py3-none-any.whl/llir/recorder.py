"""
Defines the main class of the package (LowLevelInputRecorder).
Check the package and class docstrings for more information.
"""
from typing import Callable, TypeAlias, Literal, Any, Sequence, cast
from collections import deque
import threading
import time
import os

from llir.send_input import get_cursor_position, set_cursor_position, mouse_event, keyboard_event
from llir.raw_input import register_callback, create_window_and_start_processing, destroy_window_and_stop_processing


RecordedInput: TypeAlias = (
        tuple[float, Literal["m"], int, int, int, int, int] |
        tuple[float, Literal["k"], int, int, int, int] |
        tuple[float, Literal["c"], int, int])
RecordedInputList: TypeAlias = list[RecordedInput]


class ExponentialDecay:
    def __init__(self, decay_factor: float = 0.8, max_len: int = 5) -> None:
        """
        Weighted average with exponential decay.

        Parameters
        ----------
        decay_factor : float, optional
            How much older values decay. Default is 0.8.
        max_len : int, optional
            The maximum number of past elements to consider.
        """
        self.decay_factor = decay_factor  # how much older values decay
        self.values: deque[int | float] = deque(maxlen=max_len)

    def add(self, value: int | float) -> None:
        self.values.append(value)

    def get_weighted_value(self) -> float:
        """Get the current weighted average. If no elements are added yet, 0.0 is returned."""
        weighted_sum = 0.0
        total_weight = 0.0
        for i, v in enumerate(reversed(self.values)):
            weight = self.decay_factor ** i
            weighted_sum += v * weight
            total_weight += weight
        return weighted_sum / total_weight if total_weight > 0 else 0.0


class LowLevelInputRecorder:

    """
    Record and play back low level mouse and keyboard input.

    This classes creates an "invisible" window and registers a Window Procedure to it to capture messages from the
    Windows message queue.
    The message queue is filled with messages when an event occurs like moving the mouse, clicking a button, etc.
    A raw input device is registered to the window for both the mouse and the keyboard, then a loop runs checking
    for messages of type raw input (WM_INPUT) and records any events.

    Raw Input API is used because it allows for getting mouse and keyboard events before they have been altered by
    the operating system or other software, because it sets right up the device driver.
    This is useful for recording input for use in games, since games usually use this API to get their inputs too, as
    they don't want the operating system changing the raw input data, for example mouse acceleration or keyboard layout
    shifts. If you ever wondered why WASD work even if you are using another keyboard layout or language, this is why.

    This class can be used in two different ways:
        - As a normal class: Initialize the class and call its function manually. For example, you call
          `start_listening()` then call `start_recording()` and wait for the number of seconds you want to capture
          input for (you need to wait because `start_recording()` is non-blocking)
          then after the sleep call `stop_listening()`.
        - As a listener: Initialize the class and call `start_recording`, now a non-blocking
          thread starts in the background listening for shortcuts to trigger actions, like start/stop recording.

    Methods
    -------
    start_listening()
        The main entrypoint to the class. Must be called before other actions can be done.
    start_recording()
        Start recording mouse and keyboard input.
    stop_recording()
        Stop recording mouse and keyboard input if they are already being recorded, do nothing otherwise.
    start_replaying()
        Start replaying a recorder macro from the current run, or if `start_recording` hasn't been called yet and
        `save_file_path` is specified and contains valid macro data, load and replay that instead.
    stop_recording()
        Stop replaying a macro if one is already replaying, do nothing otherwise.
    stop_listening()
        Stop listening for mouse and keyboard input, stop replaying if a macro is replaying and stop recording
        input if currently recording. Note that you can't use any other methods after this function is called until
        `start_listening` is called again.

    Notes
    -----
    - To record keyboard and mouse events and be able to replay them on a different window (application), the python
      process that ran the script must be on the same level of privilege as that application,
      with some notable exceptions.
      So for example, if you run a game as an administrator, you must also run Python (through your IDE or CMD) as an
      administrator to be able to record keyboard and mouse inputs and replay them in that window.
      A notable exception to this is Task Manager, even if you launch it normally, you need admin privileges to
      "send input" to it.
    - The only blocking function in this class is `start_replaying` for replaying back the input, the other functions
      return immediately so you will need to place `time.sleep()` calls for example after starting to record.
    - You can't use the class after you called `stop_listening` unless you call `start_listening()` again.
    - Some touchpad features aren't treated as mouse input, like gestures (3 finger input) and these events aren't
      recorded thus not played back.
    """

    def __init__(
            self, save_file_path: str = "",
            start_recording_shortcut: str = "0x001D+0x004B",  # left ctrl + left arrow
            stop_recording_shortcut: str = "0x001D+0x004D",   # left ctrl + right arrow
            start_replaying_shortcut: str = "0x001D+0x0050",  # left ctrl + down arrow
            stop_replaying_shortcut: str = "0x001D+0x0048",   # left ctrl + up arrow
            stop_shortcut: str = "0x001D+0x002A+0x002D",
            append_new_input: bool = False) -> None:
        """
        Initialize the class and define its behaviour. If you omit the start and stop recording shortcuts, you can
        only use the class manually, otherwise it can be controlled by the shortcuts.

        Parameters
        ----------
        save_file_path : str, optional
            Where to save the recorded device input. If this is an empty string (the default), input isn't saved to
            a file when recording is stopped.
        start_recording_shortcut : str, optional
            A list of `scan codes` [1]_ separated by "+" that when pressed, recording input will start.
            If it's an empty string, you can't control the class using shortcuts, and you have to call its methods
            and wait between them manually. Default is left ctrl and left arrow (the one not on the numpad).
            If a scan code for the key you want as a shortcut doesn't exist, you can use its `Virtual Key Code` [2]_.
            A list for scan codes and virtual key codes can be found in the "References" section.
        stop_recording_shortcut : str, optional
            The shortcut for stopping recording. This must be defined for `start_recording(wait_for_shortcut=True)` to
            work. Default is left ctrl and right arrow.
        start_replaying_shortcut : str, optional
            The shortcut for replaying a recorded macro from this run or from a file if no macro has been recorded yet
            and `save_file_path` is specified and contains valid input device data. Default is left ctrl and down arrow.
        stop_replaying_shortcut : str, optional
            The shortcut for stopping replaying the macro even if it hasn't finished replaying.
            Default is left ctrl and up arrow.
        stop_shortcut : str, optional
            The shortcut for stopping the listener background thread that listens for input and destroying the listening
            window, effectively shutting down the class. Default is left ctrl, left shift and the letter "X".
        append_new_input : bool, optional
            Whether to append any new device input to already recorded inputs from previous runs.
            Default is False, which means every time `start_recording` is called, any previously recorded input is
            discarded.

        References
        ----------
        .. [1] https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input#scan-codes
        .. [2] https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        """
        self.save_file_path = save_file_path
        self.start_recording_shortcut = self._convert_shortcut(start_recording_shortcut)
        self.stop_recording_shortcut = self._convert_shortcut(stop_recording_shortcut)
        self.start_replaying_shortcut = self._convert_shortcut(start_replaying_shortcut)
        self.stop_replaying_shortcut = self._convert_shortcut(stop_replaying_shortcut)
        self.stop_shortcut = self._convert_shortcut(stop_shortcut)
        self.append_new_input = append_new_input

        self.is_replaying = threading.Event()
        self.is_recording = threading.Event()
        self.has_stopped = threading.Event()
        self.has_stopped.set()

        self.recorded_device_input: RecordedInputList = []
        self._listener_thread: threading.Thread | None = None
        self._pressed_keys: set[int] = set()
        self._pressed_buttons: set[int] = set()
        self._shortcut_action_map: dict[tuple[int, ...], Callable[..., Any]] = {
            tuple(self.start_recording_shortcut): self.start_recording,
            tuple(self.stop_recording_shortcut): self.stop_recording,
            tuple(self.start_replaying_shortcut): self.start_replaying,
            tuple(self.stop_replaying_shortcut): self.stop_replaying,
            tuple(self.stop_shortcut): self.stop_listening,
        }
        self._button_up_down_mapping = {
            0x0001: 0x0002,  # Left down/up
            0x0004: 0x0008,  # Right
            0x0010: 0x0020,  # Middle
            0x0040: 0x0080,  # XBUTTON1
            0x0100: 0x0200,  # XBUTTON2
        }

        register_callback("mouse", self._mouse_callback)
        register_callback("keyboard", self._keyboard_callback)

    @staticmethod
    def _convert_shortcut(shortcut: str) -> set[int]:
        """Convert a string of scan codes in base 16 separated by + to a set of integers."""
        if not shortcut:
            return set()
        return set(map(lambda i: int(i, 16), shortcut.split("+")))

    def _save_device_input_to_file(self) -> None:
        """
        Save recorded mouse and keyboard input to `save_file_path`.

        This function does nothing of either `save_file_path` is not set or if no device input has been recorded.
        """
        if not self.save_file_path or not self.recorded_device_input:
            return
        try:
            with open(self.save_file_path, "w") as save_file:
                for single_event in self.recorded_device_input:
                    save_file.write(",".join(map(str, single_event)) + "\n")
        except FileNotFoundError:
            print(f"Can't save the recorded device data to {self.save_file_path}.")

    def _load_device_input_from_file(self) -> RecordedInputList | None:
        """
        Loads a recorded macro at `save_file_path` if the file exists and has a valid file format and return the
        recorded input list, do nothing and return None otherwise.
        """
        if not self.save_file_path or not os.path.isfile(self.save_file_path):
            return None
        recorded_device_input: RecordedInputList = []
        with open(self.save_file_path, "r") as save_file:
            try:
                for single_input in save_file.readlines():
                    input_data = single_input.split(",")
                    timestamp = float(input_data[0])
                    device = input_data[1]
                    if device not in ("m", "k", "c"):
                        raise ValueError(f"Invalid event type: {device}")
                    int_args = [int(x) for x in input_data[2:]]
                    if device == "m" and len(int_args) == 5:
                        parsed_movement = cast(RecordedInput, (timestamp, device, *int_args))
                    elif device == "k" and len(int_args) == 4:
                        parsed_movement = cast(RecordedInput, (timestamp, device, *int_args))
                    elif device == "c" and len(int_args) == 2:
                        parsed_movement = cast(RecordedInput, (timestamp, device, *int_args))
                    else:
                        raise ValueError(f"Invalid number of arguments for event type {device}")
                    recorded_device_input.append(parsed_movement)
            except (ValueError, IndexError):
                print("Failed to load recorded macro. The data in the file doesn't match the expected format.")
                return None
            except Exception as e:
                print(f"Failed to load recorded macro: {e}")
                return None
        return recorded_device_input

    def _monitor_pressed_keys(self, press: int, scan_code: int, vkey: int, _: int) -> None:
        """Callback for monitoring pressed keyboard keys."""
        if press in (0, 2):
            self._pressed_keys.add(scan_code if scan_code else vkey)
        else:
            self._pressed_keys.discard(scan_code if scan_code else vkey)

    def _monitor_pressed_buttons(self, button: int, *_: Any) -> None:
        """Callback for monitoring clicked but not released mouse buttons."""
        if self.is_replaying.is_set():
            if button == 0:  # 0 is for move events. I know not really a button.
                return
            if button in self._button_up_down_mapping.keys():
                self._pressed_buttons.add(button)
            else:
                self._pressed_buttons.discard(
                    list(self._button_up_down_mapping.keys())[list(self._button_up_down_mapping.values()).index(32)])

    def _check_shortcut_pressed(self, shortcut_keys: Sequence[int]) -> bool:
        """Return whether a shortcut is currently pressed."""
        return len(self._pressed_keys.intersection(shortcut_keys)) == len(shortcut_keys)

    def _mouse_callback(
            self, button_flgas: int, lastx: int, lasty: int, scroll_direction: int, extra_info: int) -> None:
        """
        A callback that's passed to the thread recording raw device input that will record mouse input
        only if `is_recording` flag is set.
        """
        if self.is_recording.is_set():
            self.recorded_device_input.append(
                (time.time(), "m", button_flgas, lastx, lasty, scroll_direction, extra_info))

    def _keyboard_callback(self, key_flags: int, scan_code: int, vkey: int, extra_info: int) -> None:
        """
        A callback that monitors key presses, dispatches actions if the shortcut they are associated with is pressed
        and records keyboard input if `is_recording` flag is set.
        """
        self._monitor_pressed_keys(key_flags, scan_code, vkey, extra_info)
        for shortcut in self._shortcut_action_map:
            # extra_info (ulExtraInfo for raw mosue and ExtraInfo for raw keyboard) seem to only be non-zero only
            # when they are generated "synthetically" (e.g. using `SendInput`).
            # This is very useful information because we can know that if it's present, then we are currently
            # replaying a macro, so no need to check for shortcuts that might be triggered by the recorded input.
            # This also mean that shortcuts will still work when the user types them because `extra_info` will be zero.
            if extra_info:
                break
            if self._check_shortcut_pressed(shortcut):
                # Start the shortcut processing code in another thread to not exhaust the thread responsible for
                # capturing device input events.
                threading.Thread(target=self._shortcut_action_map[shortcut]).start()
        if self.is_recording.is_set():
            self.recorded_device_input.append(
                (time.time(), "k", key_flags, scan_code, vkey, extra_info))

    def start_recording(self) -> None:
        """
        Start recording the mouse and keyboard input. This function is non-blocking.
        """
        if self.is_replaying.is_set() or self.is_recording.is_set() or self.has_stopped.is_set():
            return
        if not self.append_new_input:
            self.recorded_device_input = []
        self.recorded_device_input.append((time.time(), "c", *get_cursor_position()))
        self.is_recording.set()
        print("Started recording.")

    def stop_recording(self) -> None:
        """
        Stop recording the mouse and keyboard input and save them to `save_file_path` if it's specified.

        .. note:: This doesn't stop the background thread listening for input, for that you need call `stop_listening`.
        """
        if not self.is_recording.is_set():
            return
        self.is_recording.clear()
        self._save_device_input_to_file()
        print("Stopped recording.")

    def start_replaying(self, start_after: float = 0.) -> None:
        """
        Start replaying a recorded macro, or of no recorded macro exists from this run, try loading the macro
        saved at `save_file_path` if it's specified upon class initialization and has a valid format.

        .. note:: This function can't be used while recording input, you need to call `stop_recording()` first.

        Parameters
        ----------
        start_after : float, optional
            How many seconds to sleep before starting to replay the macro. Default is 0, which means start immediately.
        """
        if self.is_recording.is_set() or self.is_replaying.is_set() or self.has_stopped.is_set():
            return
        macro_to_play = self.recorded_device_input or self._load_device_input_from_file()
        if not macro_to_play:
            return

        if start_after:
            time.sleep(start_after)

        self.is_replaying.set()
        print("Started replaying.")
        self._replay_events_with_hybrid_wait(macro_to_play)

        # Release any pressed keys or mouse buttons that were pressed during replaying the macro but weren't released.
        for scan_code in self._pressed_keys.copy():  # To not raise RuntimeError: Set changed size during iteration.
            keyboard_event(1, scan_code)
        self._pressed_keys.clear()
        for mouse_button in self._pressed_buttons.copy():
            mouse_event(self._button_up_down_mapping[mouse_button], 0, 0, 0)

        if self.is_replaying.is_set():  # If no request to stop replaying happened, then the function finished.
            print("Finished replaying.")
        self.is_replaying.clear()

    def stop_replaying(self) -> None:
        """Stop replaying a macro if a macro is already replaying, do nothing otherwise."""
        if not self.is_replaying.is_set():
            return
        self.is_replaying.clear()
        print("Stopped replaying.")

    def start_listening(self) -> None:
        """
        Start listening for mouse and keyboard input and monitoring shortcuts. This function only starts the listener
        thread and doesn't actually record any input, for that `start_recording` needs to be called.

        Additionally, this function must be called before calling any other methods like `start_recording`
        for recording mouse and keyboard input and `start_replaying` for replaying a recorded macro.

        .. note:: This function is non-blocking, it's the caller's responsibility to stop the listener by calling
          `stop_listening()` or pressing the `stop_shortcut` when they are done listening for
          raw device input (mouse and keyboard events).
        """
        if not self.has_stopped.is_set():
            return
        self.has_stopped.clear()
        self._listener_thread = threading.Thread(target=create_window_and_start_processing)
        self._listener_thread.start()
        print("Started listening.")

    def stop_listening(self) -> None:
        """
        Stop the listener process and save the recorded input to the specified file path on class initialization.

        The call to this function might hang until a single mouse or keyboard event is fired
        (a keypress or a moving the mouse for example).
        Due to how capturing is implemented, the event processing function is blocking and if the event queue is empty,
        it will wait until there's a message, and when that happens, the Python code checks if `stop_recording` has
        been called, and if so exists out of the message processing loop.

        **Note** that this is not a problem when controlling the class with shortcuts because the listener will
        terminate as soon as the `stop_shortcut` is pressed.
        """
        self.has_stopped.set()
        self.is_recording.clear()
        self.is_replaying.clear()
        self._save_device_input_to_file()
        destroy_window_and_stop_processing()
        if self._listener_thread and self._listener_thread.is_alive():
            self._listener_thread.join()
        print("Stopped listening.")

    def _replay_events_with_hybrid_wait(self, replay_input: RecordedInputList) -> None:
        """
        Replays recorded events using a hybrid approach of short sleeps and busy-waiting
        to achieve timing accuracy.

        This method uses a combination of:
            1. Short sleep periods for efficiency when we're far from target time
            2. Busy-waiting for precise timing when close to target time
            3. Execution time compensation for subsequent events
        """
        if not replay_input:
            return

        last_timestamp = replay_input[0][0]
        trel = 0.
        tact = 0.
        exec_time_weighted = ExponentialDecay()
        # Keep a weighted average over the last 5 execution times to smooth out any potential spikes in execution time.
        for timestamp, input_device, *input_data in replay_input:

            start_loop_time = time.perf_counter()

            rel = timestamp - last_timestamp

            while diff := (rel - exec_time_weighted.get_weighted_value()) - (time.perf_counter() - start_loop_time):
                # Check for the flag inside the loop to not have to wait for a very long time if the time difference
                # between two events was long to stop replaying the macro.
                # Also, checking if threading.Event() `is_set` is somehow as fast as checking a boolean flag, and
                # needless to say is very cheap.
                if not self.is_replaying.is_set():
                    return
                if diff > 0.001:
                    time.sleep(0.0001)
                elif 0 < diff <= 0.001:
                    continue
                else:
                    break

            start_execution_time = time.perf_counter()

            if input_device == "m":
                # Honestly I don't like the `cast`, but the other methods of getting this to work in a better and a
                # "generic" way were too ugly and required too much code.
                mouse_event(
                    *cast(tuple[int, int, int, int, int], input_data), callback=self._monitor_pressed_buttons)
            elif input_device == "k":
                keyboard_event(
                    *cast(tuple[int, int, int, int], input_data), callback=self._monitor_pressed_keys)
            elif input_device == "c":
                set_cursor_position(*input_data)

            last_execution_time = time.perf_counter() - start_execution_time
            exec_time_weighted.add(last_execution_time)

            last_timestamp = timestamp

            act = time.perf_counter() - start_loop_time

            trel += rel
            tact += act

        print(f"Should've taken: {trel:.3f} - "
              f"actually taken: {tact:.3f} - "
              f"diff: {100 - trel / (tact or 1) * 100:.2f}%")


if __name__ == "__main__":
    m = LowLevelInputRecorder()
    m.start_listening()
