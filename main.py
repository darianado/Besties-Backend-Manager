# Import the necessary packages
import sys
import time
from consolemenu import *
from consolemenu.items import *
from functions import seed_database, unseed_database, get_recommendations
import platform, subprocess, json, os

from settings_reader import SettingsReader

NAME = "Backend Manager"
SETTINGS_FILENAME = "settings.json"
SEED_SETTINGS_FILENAME = "seed_settings.json"
REC_SETTINGS_FILENAME = "rec_settings.json"

settings_reader = SettingsReader()

"""
menu = ConsoleMenu(NAME, subtitle="Helper tool for developing and testing backend for the Djangoals SEG group project.", prologue_text="For Mac and Windows only.")
MAIN_SETTINGS_FILENAME = "main_settings.json"
SEED_SETTINGS_FILENAME = "seed_settings.json"
REC_SETTINGS_FILENAME = "rec_settings.json"

print("Configuring environment...")
data = json.load(open(MAIN_SETTINGS_FILENAME))

# export FIRESTORE_EMULATOR_HOST="localhost:8080"

env_var_set = os.environ.get('FIRESTORE_EMULATOR_HOST') is not None

prologue = "For Mac and Windows only.\n\r"
prologue += "Running in production mode!!\nTo run locally, exit application and run this command:\n'export FIRESTORE_EMULATOR_HOST=\"localhost:8080\"'.\nThen restart the application." if not env_var_set else "Running in local mode.\nFirebase Storage is disabled.\nTo switch, restart your terminal and this application."


menu = ConsoleMenu(NAME, subtitle="Helper tool for developing and testing backend for the Djangoals SEG group project.", prologue_text=prologue)


seeding_menu = ConsoleMenu(NAME, "Seed and unseed the database, or change settings for seeding.")

seed_settings_item = CommandItem("Open settings in VSCode", f"code {SEED_SETTINGS_FILENAME}" if platform.system() == "Windows" else f"open -a 'Visual Studio Code.app' {SEED_SETTINGS_FILENAME}")
seed_item = FunctionItem("Seed", seed_database)
unseed_item = FunctionItem("Unseed", unseed_database)

seeding_menu.append_item(seed_settings_item)
seeding_menu.append_item(seed_item)
seeding_menu.append_item(unseed_item)

seeding_item = SubmenuItem("Seed/Unseed database", seeding_menu, menu)

recommendation_menu = ConsoleMenu(NAME, "Send recommendation requests, or change settings for the request.")

rec_settings_item = CommandItem("Open settings in VSCode", f"code {REC_SETTINGS_FILENAME}" if platform.system() == "Windows" else f"open -a 'Visual Studio Code.app' {REC_SETTINGS_FILENAME}")
rec_item = FunctionItem("Get Recommendations", get_recommendations)

recommendation_menu.append_item(rec_settings_item)
recommendation_menu.append_item(rec_item)

recommendation_item = SubmenuItem("Recommendations", recommendation_menu, menu)

menu.append_item(seeding_item)
menu.append_item(recommendation_item)

menu.show()
"""