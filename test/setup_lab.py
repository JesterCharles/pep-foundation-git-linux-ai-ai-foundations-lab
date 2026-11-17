"""Create (or reset) the review desk in src/review-desk/.

Run from the lab folder:  python test/setup_lab.py
Re-running it is the reset path: it removes your work/ folder and restores
the shipped files.
"""

import sys
from pathlib import Path

# Run as a script (python test/setup_lab.py): put the project folder on the import
# path so the shared helpers load as test.lab_support, the name pytest uses.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from test.lab_support import WORK, reset_starter


def main():
    if sys.version_info < (3, 11):
        sys.exit("Python 3.11 or newer is required. Check `python --version`.")

    if WORK.exists():
        print("WARNING: resetting the lab. Everything inside work/ is removed.")
    reset_starter()
    WORK.mkdir(parents=True, exist_ok=True)

    print("Review desk ready in src/review-desk/.")
    print("Next: cd src/review-desk, then read USER_STORY.md.")


if __name__ == "__main__":
    main()
