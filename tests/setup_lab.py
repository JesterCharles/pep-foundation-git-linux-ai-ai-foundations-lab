"""Create (or reset) the review desk in starter/review-desk/.

Run from the lab folder:  python tests/setup_lab.py
Re-running it is the reset path: it removes your work/ folder and restores
the shipped files.
"""

import sys

from lab_support import WORK, reset_starter


def main():
    if sys.version_info < (3, 11):
        sys.exit("Python 3.11 or newer is required. Check `python --version`.")

    if WORK.exists():
        print("WARNING: resetting the lab. Everything inside work/ is removed.")
    reset_starter()
    WORK.mkdir(parents=True, exist_ok=True)

    print("Review desk ready in starter/review-desk/.")
    print("Next: cd starter/review-desk, then read USER_STORY.md.")


if __name__ == "__main__":
    main()
