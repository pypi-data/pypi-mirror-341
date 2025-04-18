import subprocess
from sodatools import CD
from pathlib import Path


def main():
    cr = Path(__file__).resolve().parent
    with CD(cr):
        try:
            subprocess.run("uvicorn bio_showcase.asgi:application", shell=True, check=False)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
