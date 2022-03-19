import time
from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *

from constants import (APPLICATION_DESCRIPTION, APPLICATION_NAME,
                       EPILOGUE_TEXT, SETTINGS_FILENAME)
from decorators import safe_exit, sleepy_exit
from environment_analyzer import EnvironmentAnalyzer
from functions import Functions
from utils import load_settings

def main():
  environment_analyzer = EnvironmentAnalyzer()
  settings = load_settings()
  functions = Functions(settings)

  # Define menus
  main_menu = generate_menu(environment_analyzer)
  seed_menu = generate_menu(environment_analyzer)
  recommendations_menu = generate_menu(environment_analyzer)

  # Define items
  settings_item = CommandItem("Open settings in VSCode", environment_analyzer.get_command_for_opening_file_in_environment(SETTINGS_FILENAME))
  seed_item = FunctionItem("Seed", functions.seed)
  unseed_item = FunctionItem("Unseed", functions.unseed)

  recommendation_item = FunctionItem("Get Recommendations", functions.get_recommendations)

  # Populate menus
  seed_menu.append_item(settings_item)
  seed_menu.append_item(seed_item)
  seed_menu.append_item(unseed_item)
  seed_submenu = SubmenuItem("Seed/Unseed", seed_menu, main_menu)

  recommendations_menu.append_item(settings_item)
  recommendations_menu.append_item(recommendation_item)
  recommendations_submenu = SubmenuItem("Recommendations", seed_menu, main_menu)

  main_menu.append_item(seed_submenu)
  main_menu.append_item(recommendations_submenu)

  # Show menu.
  main_menu.show()


def create_prologue(environment_analyzer: EnvironmentAnalyzer):
  result = environment_analyzer.get_environment_description()
  result += "\n"
  result += environment_analyzer.get_available_features_description()
  return result


def generate_menu(environment_analyzer: EnvironmentAnalyzer):
  return ConsoleMenu(APPLICATION_NAME,
                     subtitle=APPLICATION_DESCRIPTION,
                     prologue_text=create_prologue(environment_analyzer),
                     epilogue_text=EPILOGUE_TEXT,
                     formatter=MenuFormatBuilder()
                     .set_title_align('center')
                     .set_subtitle_align('center')
                     .set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_BORDER)
                     .show_prologue_top_border(True)
                     .show_prologue_bottom_border(True))

main()