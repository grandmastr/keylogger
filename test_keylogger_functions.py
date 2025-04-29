#!/usr/bin/env python3
"""
Test script to verify the keylogger.py functions work correctly.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath('.'))

# Import the functions from keylogger.py
from keylogger.keylogger import load_data, save_data, on_press, on_release, DATA_FILE


class TestKeyloggerFunctions(unittest.TestCase):
    """Test cases for the keylogger functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Save the original DATA_FILE value
        self.original_data_file = DATA_FILE
        # Use a test data file
        self.test_data_file = "test_key_counts.json"
        # Clean up any existing test files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    @patch('keylogger.keylogger.DATA_FILE', 'test_key_counts.json')
    def test_load_data_nonexistent_file(self):
        """Test that load_data returns an empty dict when the file doesn't exist."""
        data = load_data()
        self.assertEqual(data, {})

    @patch('keylogger.keylogger.DATA_FILE', 'test_key_counts.json')
    def test_load_data_existing_file(self):
        """Test that load_data loads data from an existing file."""
        # Create a test file with some data
        test_data = {"2023-01-01": 10}
        with open(self.test_data_file, "w") as f:
            json.dump(test_data, f)

        # Load the data
        data = load_data()
        self.assertEqual(data, test_data)

    @patch('keylogger.keylogger.DATA_FILE', 'test_key_counts.json')
    def test_load_data_invalid_json(self):
        """Test that load_data handles invalid JSON gracefully."""
        # Create a test file with invalid JSON
        with open(self.test_data_file, "w") as f:
            f.write("invalid json")

        # Load the data
        data = load_data()
        self.assertEqual(data, {})

    @patch('keylogger.keylogger.DATA_FILE', 'test_key_counts.json')
    def test_save_data(self):
        """Test that save_data saves data to a file."""
        # Save some data
        test_data = {"2023-01-01": 10}
        save_data(test_data)

        # Check that the file exists and contains the correct data
        self.assertTrue(os.path.exists(self.test_data_file))
        with open(self.test_data_file, "r") as f:
            data = json.load(f)
        self.assertEqual(data, test_data)

    @patch('keylogger.keylogger.key_counts', {})
    @patch('keylogger.keylogger.save_data')
    @patch('datetime.datetime')
    def test_on_press(self, mock_datetime, mock_save_data):
        """Test that on_press updates key_counts and calls save_data."""
        # Mock datetime.now() to return a fixed date
        mock_now = MagicMock()
        mock_now.strftime.return_value = "2023-01-01"
        mock_datetime.now.return_value = mock_now

        # Call on_press multiple times
        for _ in range(9):
            on_press("test_key")

        # Check that key_counts was updated
        from keylogger.keylogger import key_counts
        self.assertEqual(key_counts["2023-01-01"], 9)

        # save_data should not have been called yet
        mock_save_data.assert_not_called()

        # Call on_press one more time to reach 10
        on_press("test_key")

        # Check that key_counts was updated
        self.assertEqual(key_counts["2023-01-01"], 10)

        # save_data should have been called
        mock_save_data.assert_called_once_with(key_counts)

    @patch('keylogger.keylogger.key_counts', {"2023-01-01": 5})
    @patch('keylogger.keylogger.save_data')
    def test_on_release_normal_key(self, mock_save_data):
        """Test that on_release returns None for normal keys."""
        # Create a mock key that is not ESC
        mock_key = MagicMock()
        mock_key.__eq__.return_value = False

        # Call on_release
        result = on_release(mock_key)

        # Check that it returned None
        self.assertIsNone(result)

        # save_data should not have been called
        mock_save_data.assert_not_called()

    @patch('keylogger.keylogger.key_counts', {"2023-01-01": 5})
    @patch('keylogger.keylogger.save_data')
    @patch('builtins.print')
    def test_on_release_esc_key(self, mock_print, mock_save_data):
        """Test that on_release returns False for ESC key."""
        # Create a mock ESC key
        from pynput.keyboard import Key
        mock_key = Key.esc

        # Call on_release
        result = on_release(mock_key)

        # Check that it returned False
        self.assertFalse(result)

        # save_data should have been called
        mock_save_data.assert_called_once_with({"2023-01-01": 5})

        # print should have been called
        mock_print.assert_called_once_with("\nExiting and saving...")


def run_tests():
    """Run the test suite."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    try:
        print("Running Keylogger function tests...")
        run_tests()
        print("\nAll tests completed successfully!")
    except ImportError as e:
        print(f"ERROR: Failed to import keylogger functions: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        sys.exit(1)
