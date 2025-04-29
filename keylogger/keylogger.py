import os
import json
from datetime import datetime
from pynput import keyboard

DATA_FILE = "key_count.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


class Keylogger:
    """
    A class for recording keyboard inputs.
    """

    def __init__(self, log_file="keylog.txt"):
        """
        Initialize the keylogger with a log file.

        Args:
            log_file (str): Path to the log file where keystrokes will be recorded.
        """
        self.log_file = log_file
        self.listener = None
        self.key_counts = load_data()

    def on_press(self, key):
        """
        Callback function for key press events.

        Args:
            key: The key that was pressed.
        """
        try:
            # Log the key press to the file
            with open(self.log_file, "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp}: {key}\n")

            # Update key counts
            today = datetime.now().strftime("%Y-%m-%d")
            if today not in self.key_counts:
                self.key_counts[today] = 0
            self.key_counts[today] += 1

            if self.key_counts[today] % 10 == 0:
                save_data(self.key_counts)

        except Exception as e:
            print(f"Error logging key: {e}")

    def on_release(self, key):
        """
        Callback function for key release events.

        Args:
            key: The key that was released.
        """
        if key == keyboard.Key.esc and hasattr(self, 'stop_on_esc') and self.stop_on_esc:
            save_data(self.key_counts)
            print("\nExiting and saving key counts...")
            return False
        return None

    def log_key(self, key_text):
        """
        Manually log a key.

        Args:
            key_text (str): Text representation of the key to log.
        """
        try:
            # Ensure the directory exists
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                print(f"Warning: Directory {log_dir} does not exist. Cannot log key.")
                return

            with open(self.log_file, "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp}: {key_text}\n")
        except Exception as e:
            print(f"Error logging key: {e}")

    def start(self, stop_on_esc=True):
        """
        Start the keylogger.

        Args:
            stop_on_esc (bool): Whether to stop the keylogger when Esc is pressed.
        """
        self.stop_on_esc = stop_on_esc
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def stop(self):
        """
        Stop the keylogger.
        """
        if self.listener:
            self.listener.stop()
            # Wait for the listener to actually stop
            self.listener.join()
            save_data(self.key_counts)


def main():
    """
    Main function to run the keylogger from the command line.
    """
    print("Starting keylogger. Press Esc to exit.")
    keylogger = Keylogger()
    keylogger.start()

    # Keep the main thread alive
    try:
        while keylogger.listener.is_alive():
            keylogger.listener.join(0.1)
    except KeyboardInterrupt:
        print("\nKeylogger stopped by user.")
    finally:
        keylogger.stop()


if __name__ == "__main__":
    main()
