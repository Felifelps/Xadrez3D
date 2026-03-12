import os
from pathlib import Path
import platform


def run(command):
    print(">", command)
    os.system(command)

venv_path = Path(".venv")
is_windows = "Windows" in platform.platform(terse=True)

python = "python" + ("" if is_windows else "3")
venv_activate_command = f"{venv_path}\\Scripts\\Activate" if is_windows else f"source {venv_path}/bin/activate"

if not venv_path.exists():
    run(f"{python} -m venv {venv_path}")

run(venv_activate_command)
run("pip install -r requirements.txt")

run(f"{python} main.py")
