import os
from glob import glob
from dotenv import dotenv_values
from .util import color_text
from .constants import FAIL


def find_key_file(keyfile_dir: str, keyfile_glob: str):
    key_files = glob(f"{keyfile_dir}/{keyfile_glob}")
    if not key_files:
        print(color_text("No service account key file found", FAIL))
        return None
    return key_files[0]


def find_env_file():
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):
        env_path = os.path.join(current_dir, ".env")
        if os.path.isfile(env_path):
            return env_path
        current_dir = os.path.dirname(current_dir)
    print(color_text(".env file not found", FAIL))
    return None


def load_env_variables(env_file):
    return dotenv_values(env_file)
