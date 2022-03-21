from enums import RunMode
from alive_progress.animations.bars import bar_factory
from alive_progress.animations.spinners import bouncing_spinner_factory

APPLICATION_NAME = "Firebase Backend Manager"
APPLICATION_DESCRIPTION = "Tool for testing production and deployment candidates of Firebase products used."
EPILOGUE_TEXT = "2022 © Copyright Djangoals"

SETTINGS_FILENAME = "settings.json"

FIREBASE_FIRESTORE_EMULATOR_ENV_VAR = "FIRESTORE_EMULATOR_HOST"
FIREBASE_FIRESTORE_EMULATOR_ENV_VAR_VALUE = "localhost:8080"
FIREBASE_AUTH_EMULATOR_ENV_VAR = "FIREBASE_AUTH_EMULATOR_HOST"
FIREBASE_AUTH_EMULATOR_ENV_VAR_VALUE = "localhost:9099"

FIREBASE_CREDENTIALS_FILE = 'serviceAccountKey.json'
FIREBASE_STORAGE_BUCKET = 'seg-djangoals.appspot.com'

FIRESTORE_BATCH_SIZE = 500

SLEEPY_EXIT_DURATION = 3


FIRESTORE_RUN_MODES = [RunMode.EMULATOR, RunMode.PRODUCTION]
AUTH_RUN_MODES = [RunMode.EMULATOR, RunMode.PRODUCTION]
STORAGE_RUN_MODES = [RunMode.PRODUCTION]

CIRCLES_BAR = bar_factory('●', background='○', borders="||")
CIRCLES_BAR_SPINNER = bouncing_spinner_factory(chars='●', background='○', length=10, block=5)