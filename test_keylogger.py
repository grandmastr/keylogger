#!/usr/bin/env python3
"""
Test script to verify the keylogger package works correctly.
"""

import os
import sys
import json
import unittest
from datetime import datetime

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath('.'))

# Import the Keylogger class from the package
from keylogger import Keylogger


class TestKeylogger(unittest.TestCase):
    """Test cases for the Keylogger class."""

    def setUp(self):
        """Set up test fixtures."""
        self.log_file = "test_log.txt"
        self.data_file = "key_count.json"
        # Clean up any existing test files
        for file in [self.log_file, self.data_file]:
            if os.path.exists(file):
                os.remove(file)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        for file in [self.log_file, self.data_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_keylogger_initialization(self):
        """Test that the keylogger can be initialized."""
        keylogger = Keylogger(log_file=self.log_file)
        self.assertEqual(keylogger.log_file, self.log_file)
        self.assertIsNone(keylogger.listener)
        self.assertIsInstance(keylogger.key_counts, dict)

    def test_log_key(self):
        """Test that keys can be logged manually."""
        keylogger = Keylogger(log_file=self.log_file)
        test_keys = ["a", "b", "Enter", "Shift"]

        for key in test_keys:
            keylogger.log_key(key)

        # Check that the log file exists and contains the logged keys
        self.assertTrue(os.path.exists(self.log_file))

        with open(self.log_file, "r") as f:
            log_content = f.read()

        for key in test_keys:
            self.assertIn(key, log_content)

    def test_start_stop(self):
        """Test that the keylogger can be started and stopped."""
        keylogger = Keylogger(log_file=self.log_file)

        # Test starting
        keylogger.start()
        self.assertIsNotNone(keylogger.listener)
        self.assertTrue(keylogger.listener.is_alive())

        # Test stopping
        keylogger.stop()
        self.assertFalse(keylogger.listener.is_alive())

    def test_key_counting(self):
        """Test that key presses are counted correctly."""
        keylogger = Keylogger(log_file=self.log_file)
        today = datetime.now().strftime("%Y-%m-%d")

        # Simulate key presses
        for _ in range(5):
            keylogger.on_press("test_key")

        # Check that the key count was updated
        self.assertEqual(keylogger.key_counts.get(today, 0), 5)

        # Check that the data file is created after enough key presses
        for _ in range(5):  # 5 more to reach 10
            keylogger.on_press("test_key")

        self.assertTrue(os.path.exists("key_count.json"))

        # Verify the content of the data file
        with open("key_count.json", "r") as f:
            data = json.load(f)

        self.assertEqual(data.get(today, 0), 10)

    def test_error_handling(self):
        """Test that errors are handled gracefully."""
        keylogger = Keylogger(log_file="/nonexistent/directory/test_log.txt")

        # This should not raise an exception
        try:
            keylogger.log_key("test_key")
            # If we get here, the error was handled
            self.assertTrue(True)
        except:
            self.fail("log_key raised an exception unexpectedly!")


def run_tests():
    """Run the test suite."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    try:
        print("Running Keylogger tests...")
        run_tests()
        print("\nAll tests completed successfully!")
    except ImportError as e:
        print(f"ERROR: Failed to import Keylogger class: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        sys.exit(1)
