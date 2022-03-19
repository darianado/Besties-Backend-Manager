import json
import os
import platform
from types import SimpleNamespace

from constants import FIREBASE_CREDENTIALS_FILE, FIREBASE_STORAGE_BUCKET, SETTINGS_FILENAME
from enums import Platform, RunMode
import firebase_admin
from firebase_admin import credentials, firestore, storage


def load_settings():
  try:
    return json.load(open(SETTINGS_FILENAME), object_hook=lambda d: SimpleNamespace(**d))
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


def initialize_firebase():
  cred = credentials.Certificate(FIREBASE_CREDENTIALS_FILE)
  firebase_admin.initialize_app(cred, {
    'storageBucket': FIREBASE_STORAGE_BUCKET,
  })