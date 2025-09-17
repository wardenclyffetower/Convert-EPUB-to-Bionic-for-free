import unittest
import subprocess
import sys

class TestBionic(unittest.TestCase):
    def test_no_args_shows_help(self):
        """
        Tests that running the script with no arguments prints the help message.
        """
        process = subprocess.run(
            [sys.executable, "bionic.py"],
            capture_output=True,
            text=True,
        )
        self.assertIn("usage: bionic.py [-h] book_path", process.stderr)
        self.assertEqual(process.returncode, 2)

if __name__ == "__main__":
    unittest.main()