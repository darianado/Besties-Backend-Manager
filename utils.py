import json

import firebase_admin
from firebase_admin import credentials

from constants import (FIREBASE_CREDENTIALS_FILE, FIREBASE_STORAGE_BUCKET,
                       SETTINGS_FILENAME)

from pathlib import Path

def load_settings():
  try:
    return json.load(open(SETTINGS_FILENAME))
  except:
    print(f"""ERROR: Could not load settings file. 
          Please check that a file by the name \'{SETTINGS_FILENAME}\' exists, 
          and contains properly formatted json.""")

# https://stackoverflow.com/questions/21035762/python-read-json-file-and-modify
def update_settings_field(field: str, value):
  with open(SETTINGS_FILENAME, 'r+') as f:
    data = json.load(f)
    data[field] = value # <--- add `id` value.
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)
    f.truncate()


def _check_file_exists(path: str):
  return Path(path).is_file()

def initialize_firebase():
  certificate_exists = _check_file_exists(FIREBASE_CREDENTIALS_FILE)

  if(not certificate_exists):
    raise FileNotFoundError(f"""ERROR: Could not load settings file. 
          Please check that a file by the name \'{FIREBASE_CREDENTIALS_FILE}\' exists.""")

  cred = credentials.Certificate(FIREBASE_CREDENTIALS_FILE)
  firebase_admin.initialize_app(cred, {
    'storageBucket': FIREBASE_STORAGE_BUCKET,
  })
