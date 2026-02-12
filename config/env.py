import os

def is_wsl():
    return "WSL_DISTRO_NAME" in os.environ
