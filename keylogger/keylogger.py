import os
import json
from datetime import datetime
from pynput import keyboard

# Path to store daily key counts
DATA_FILE = "key_counts.json"

# Load existing data or initialize empty
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Save updated data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Setup initial data
key_counts = load_data()

def on_press(key):
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in key_counts:
        key_counts[today] = 0
    key_counts[today] += 1

    # Save every 10 keystrokes to avoid file write on every key
    if key_counts[today] % 10 == 0:
        save_data(key_counts)

def on_release(key):
    # quit on ESC
    if key == keyboard.Key.esc:
        save_data(key_counts)
        print("\nExiting and saving...")
        return False
    return None

# Listen for keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
