# Keylogger

A simple Python package for recording keyboard inputs with timestamp tracking and key press counting.

## Disclaimer

This package is intended for educational purposes only. Using a keylogger to record someone's keystrokes without their knowledge or consent may be illegal and unethical. Always ensure you have proper authorization before monitoring keyboard activity.

## Installation

You can install the package directly from GitHub:

```bash
pip install git+https://github.com/grandmastr/keylogger.git
```

Or after cloning the repository:

```bash
git clone https://github.com/grandmastr/keylogger.git
cd keylogger
pip install .
```

## Usage

### Basic Usage

```python
from keylogger import Keylogger

# Create a keylogger instance
keylogger = Keylogger(log_file="my_log.txt")

# Start the keylogger
keylogger.start()

# The keylogger is now running in the background
# To stop it:
keylogger.stop()
```

### Command Line Usage

The package also provides a command-line interface:

```bash
keylogger
```

This will start the keylogger with default settings and log to `keylog.txt` in the current directory. Press the Esc key to stop the keylogger when running from the command line.

### Manual Key Logging

You can also manually log keys without capturing keyboard events:

```python
from keylogger import Keylogger

keylogger = Keylogger(log_file="manual_log.txt")
keylogger.log_key("Custom event")
```

## Features

- Simple and easy-to-use API
- Logs keystrokes with timestamps
- Configurable log file location
- Tracks daily key press counts in a JSON file
- Option to stop the keylogger when Esc is pressed
- Command-line interface for quick usage
- Error handling for file operations

## Requirements

- Python 3.6 or higher
- pynput >= 1.7.6

## Data Files

- **Log File**: Records each keystroke with a timestamp (default: `keylog.txt`)
- **Key Count File**: Tracks the number of key presses per day in JSON format (`key_count.json`)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
