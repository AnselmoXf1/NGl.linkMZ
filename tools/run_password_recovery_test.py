import sys
import os

# Ensure project root is on sys.path so we can import the test module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_password_recovery import test_password_recovery


if __name__ == '__main__':
    test_password_recovery()
