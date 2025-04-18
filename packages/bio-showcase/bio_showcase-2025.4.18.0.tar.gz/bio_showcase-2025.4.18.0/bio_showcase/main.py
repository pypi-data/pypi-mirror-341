import subprocess


def main():
    subprocess.run("uvicorn bio_showcase.asgi:application", shell=True, check=False)


if __name__ == "__main__":
    main()
