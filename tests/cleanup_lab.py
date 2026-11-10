"""Remove everything the lab created.

Run from the lab folder:  python tests/cleanup_lab.py
It removes starter/review-desk/work/ and the Python cache in tests/, then
restores the shipped starter files. It touches nothing outside this lab folder.
"""

from lab_support import reset_starter


def main():
    reset_starter()
    print("Lab cleaned: the work/ folder is removed and the shipped files are restored.")
    print("Run python tests/setup_lab.py to start again.")


if __name__ == "__main__":
    main()
