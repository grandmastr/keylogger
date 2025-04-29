# Keylogger

A simple Python package for recording keyboard inputs.

## Disclaimer

This package is intended for educational purposes only. Using a keylogger to record someone's keystrokes without their knowledge or consent may be illegal and unethical. Always ensure you have proper authorization before monitoring keyboard activity.

## Installation

You can install the package directly from GitHub:

```bash
pip install git+https://github.com/username/keylogger.git
```

Or after cloning the repository:

```bash
git clone https://github.com/username/keylogger.git
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

This will start the keylogger with default settings and log to `keylog.txt` in the current directory.

## Features

- Simple and easy-to-use API
- Logs keystrokes with timestamps
- Configurable log file location

## Requirements

- Python 3.6 or higher

## License

This project is licensed under the MIT License - see the LICENSE file for details.
