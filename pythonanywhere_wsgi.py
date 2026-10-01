"""PythonAnywhere WSGI entrypoint for Hamed AGI."""
import os
import sys

PROJECT_DIR = "/home/aboaita2011/hamed-agi"
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)
os.chdir(PROJECT_DIR)

from cloud_server import app as application

__all__ = ["application"]
