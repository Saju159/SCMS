import os
from sys import platform

def getBaseConfigDir():
    if 'SUDO_USER' in os.environ:
        home = pwd.getpwnam(os.environ['SUDO_USER']).pw_dir
    else:
        home = os.path.expanduser("~")

    if platform == "linux":
        xdg = os.environ.get("XDG_CONFIG_HOME")
        if xdg:
            configPath = os.path.join(xdg, "SCMS")
        else:
            configPath = os.path.join(home, ".config", "SCMS")
    elif platform == "win32":
        configPath = os.path.join(home, "AppData", "Roaming", "SCMS")
    else:
        configPath = os.path.join(home, ".SCMS")

    os.makedirs(configPath, exist_ok=True)
    return configPath