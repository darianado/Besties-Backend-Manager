import json
import os
import platform
from types import SimpleNamespace

from constants import SETTINGS_FILENAME
from enums import Platform, RunMode


def load_settings():
  try:
    return json.load(open(SETTINGS_FILENAME), object_hook=lambda d: SimpleNamespace(**d))
  except:
    print(f"""ERROR: Could not load settings file. 
          Please check that a file by the name \'{SETTINGS_FILENAME}\' exists, 
          and contains properly formatted json.""")