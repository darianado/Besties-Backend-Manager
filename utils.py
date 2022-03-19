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


def initialize_firebase():
  cred = credentials.Certificate(FIREBASE_CREDENTIALS_FILE)
  firebase_admin.initialize_app(cred, {
    'storageBucket': FIREBASE_STORAGE_BUCKET,
  })