import os
import sys

from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *

from constants import (APPLICATION_DESCRIPTION, APPLICATION_NAME,
                       EPILOGUE_TEXT, SETTINGS_FILENAME)
from environment_manager import EnvironmentManager
from functions import Functions
from services.services_manager import ServicesManager


class Runner:

  def __init__(self):
    self.environment_manager = EnvironmentManager()
    self.services_manager = ServicesManager(self.environment_manager)
    self.functions = Functions(self.environment_manager, self.services_manager)

    self.show_menu(self.environment_manager, self.functions)

  def switch_run_mode(self):
    self.environment_manager.switch_run_mode()
    os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)  # To hard-restart this app

  def show_menu(self, environment_manager: EnvironmentManager, functions: Functions):
    # Define menus
    main_menu = self._generate_menu(environment_manager)
    seed_menu = self._generate_menu(environment_manager)
    recommendations_menu = self._generate_menu(environment_manager)
    matching_menu = self._generate_menu(environment_manager)

    # Define items
    settings_item = CommandItem("Open settings in VSCode", environment_manager.get_command_for_opening_file_in_environment(SETTINGS_FILENAME))
    seed_item = FunctionItem("Seed", functions.seed)
    unseed_item = FunctionItem("Unseed", functions.unseed)

    env_item = FunctionItem("Switch run mode", self.switch_run_mode, should_exit=True)

    recommendation_item = FunctionItem("Get Recommendations", functions.get_recommendations)

    like_user_item = FunctionItem("Like a user", functions.like_user)

    # Populate menus
    seed_menu.append_item(settings_item)
    seed_menu.append_item(seed_item)
    seed_menu.append_item(unseed_item)
    seed_submenu = SubmenuItem("Seed/Unseed", seed_menu, main_menu)

    recommendations_menu.append_item(settings_item)
    recommendations_menu.append_item(recommendation_item)
    recommendations_submenu = SubmenuItem("Recommendations", recommendations_menu, main_menu)

    matching_menu.append_item(like_user_item)
    matching_submenu = SubmenuItem("Matching", matching_menu, main_menu)

    main_menu.append_item(seed_submenu)
    main_menu.append_item(recommendations_submenu)
    main_menu.append_item(matching_submenu)
    main_menu.append_item(env_item)

    # Show menu.
    main_menu.show()


  def _create_prologue(self, environment_manager: EnvironmentManager):
    result = environment_manager.get_environment_description()
    result += "\n"
    result += self.services_manager.get_available_features_description()
    return result


  def _generate_menu(self, environment_manager: EnvironmentManager):
    return ConsoleMenu(APPLICATION_NAME,
                      subtitle=APPLICATION_DESCRIPTION,
                      prologue_text=self._create_prologue(environment_manager),
                      epilogue_text=EPILOGUE_TEXT,
                      formatter=MenuFormatBuilder()
                      .set_title_align('center')
                      .set_subtitle_align('center')
                      .set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_BORDER)
                      .show_prologue_top_border(True)
                      .show_prologue_bottom_border(True))

Runner()
