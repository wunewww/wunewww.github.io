import sys
import subprocess


def main():
    subprocess.check_call([sys.executable, '-m', 'uvx', 'hugo'])


if __name__ == "__main__":
    main()
