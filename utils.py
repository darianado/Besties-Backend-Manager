import json
import random
from pathlib import Path
from typing import List

import firebase_admin
from firebase_admin import credentials

from constants import (FIREBASE_CREDENTIALS_FILE, FIREBASE_STORAGE_BUCKET,
                       SETTINGS_FILENAME)


def pick_random_pairs(self, n: int, lst: List):
  """Picks n number of random pairs from the supplied list. Each pair contains two distinct elements."""
  result = []

  while(n > 0):
    result.append(random.sample(lst, 2))
    n -= 1

  return result

def load_settings():
  """Loads the settings file. Will raise a FileNotFoundError if the file cannot be found."""
  try:
    return json.load(open(SETTINGS_FILENAME))
  except:
    raise FileNotFoundError(f"""ERROR: Could not load settings file. 
          Please check that a file by the name \'{SETTINGS_FILENAME}\' exists, 
          and contains properly formatted json.""")


def update_settings_field(field: str, value):
  """Updates the value for a field in a json file, and saves the result."""
  with open(SETTINGS_FILENAME, 'r+') as f:
    data = json.load(f)
    data[field] = value
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()


def _check_file_exists(path: str):
  """Returns True if a file exists at the specified path."""
  return Path(path).is_file()


def initialize_firebase():
  """Initializes Firebase using the Service Account key file. Will raise a FileNotFoundError if the file cannot be found."""
  certificate_exists = _check_file_exists(FIREBASE_CREDENTIALS_FILE)

  if(not certificate_exists):
    raise FileNotFoundError(f"""ERROR: Could not load settings file. 
          Please check that a file by the name \'{FIREBASE_CREDENTIALS_FILE}\' exists.""")

  cred = credentials.Certificate(FIREBASE_CREDENTIALS_FILE)
  firebase_admin.initialize_app(cred, {
    'storageBucket': FIREBASE_STORAGE_BUCKET,
  })
