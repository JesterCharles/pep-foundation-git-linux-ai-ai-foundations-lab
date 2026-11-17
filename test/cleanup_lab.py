"""Remove everything the lab created.

Run from the lab folder:  python test/cleanup_lab.py
It removes src/review-desk/work/ and the Python cache in test/, then
restores the shipped starter files. It touches nothing outside this lab folder.
"""

import sys
from pathlib import Path

# Run as a script (python test/cleanup_lab.py): put the project folder on the import
# path so the shared helpers load as test.lab_support, the name pytest uses.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from test.lab_support import reset_starter


def main():
    reset_starter()
    print("Lab cleaned: the work/ folder is removed and the shipped files are restored.")
    print("Run python test/setup_lab.py to start again.")


if __name__ == "__main__":
    main()
