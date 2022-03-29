import os
import platform

from colors import color

from constants import (FIREBASE_AUTH_EMULATOR_ENV_VAR,
                       FIREBASE_AUTH_EMULATOR_ENV_VAR_VALUE,
                       FIREBASE_FIRESTORE_EMULATOR_ENV_VAR,
                       FIREBASE_FIRESTORE_EMULATOR_ENV_VAR_VALUE)
from enums import Platform, RunMode
from utils import initialize_firebase, load_settings, update_settings_field


class EnvironmentManager:
  """Class responsible for collecting and storing information about the environment in 
  which the application is running. As such, this class contains methods that other 
  classes can query to determine what actions they can carry out in the given environment. 
  The class also contains methods to describe the environment to the user."""

  def __init__(self):
    self.settings = load_settings()
    self.platform_type = self._analyze_platform()
    self.run_mode = self._configure_run_mode()
    self._setup_environment_for_run_mode()
    initialize_firebase()

  def _analyze_platform(self):
    """This function analyses the platform the application is running on."""
    platform_type = platform.system()
    
    if(platform_type == "Darwin"):
      return Platform.MACOS
    elif(platform_type == "Linux"):
      return Platform.LINUX
    else:
      return platform_type

  def _configure_run_mode(self):
    """Reads the settings file section 'emulator_run_mode' and returns the appropriate RunMode."""
    if(self.settings["emulator_run_mode"]):
      return RunMode.EMULATOR
    else:
      return RunMode.PRODUCTION

  def _get_os_environment_description(self):
    """Returns a humanized string describing if the current platform is supported."""
    if(self.platform_type == Platform.MACOS or self.platform_type == Platform.LINUX):
      return color("[✔]", fg="green") + f" {self.platform_type.value} is supported."
    else:
      return color("[✘]", fg="red") + f" {self.platform_type} is not supported."


  def _get_run_mode_description(self):
    """Returns a humanized string describing the current RunMode."""
    if(self.run_mode == RunMode.EMULATOR):
      return color("[✔]", fg="green") + """ Emulator mode."""
    elif(self.run_mode == RunMode.PRODUCTION):
      return color("[!]", fg="orange") + f""" Production mode. 
                                        \n    {color("BE CAREFUL; YOU ARE ALTERING THE PRODUCTION ENVIRONMENT!", fg="red")}"""
    else:
      return color("[✘]", fg="red") + f""" ERROR: Inconsistent run mode.
                                    \n    {color("Switch to emulator mode below!", fg="red")}"""

  def get_environment_description(self):
    """Collects and returns a humanized string describing the environment in full."""
    result = "Your environment:\n"
    result += self._get_os_environment_description()
    result += "\n"
    result += self._get_run_mode_description()
    return result

  def get_command_for_opening_file_in_environment(self, filename):
    """Returns the command required for opening a specific file on the platform."""
    if(self.platform_type == Platform.MACOS):
      return f"open -a 'Visual Studio Code.app' {filename}"
    elif(self.platform_type == Platform.LINUX):
      return f"gedit {filename}"
    else:
      return f"open {filename}"

  def _setup_environment_for_run_mode(self):
    """Sets required environment variables depending on RunMode."""
    if(not self.run_mode == RunMode.PRODUCTION):
      os.environ[FIREBASE_AUTH_EMULATOR_ENV_VAR] = FIREBASE_AUTH_EMULATOR_ENV_VAR_VALUE
      os.environ[FIREBASE_FIRESTORE_EMULATOR_ENV_VAR] = FIREBASE_FIRESTORE_EMULATOR_ENV_VAR_VALUE
    else:
      os.environ.pop(FIREBASE_AUTH_EMULATOR_ENV_VAR, None)
      os.environ.pop(FIREBASE_FIRESTORE_EMULATOR_ENV_VAR, None)

  def switch_run_mode(self):
    """Switches the RunMode to the opposite of what it currently is, and saves the change to the settings."""
    if(self.run_mode == RunMode.EMULATOR):
      update_settings_field("emulator_run_mode", False)
    else:
      update_settings_field("emulator_run_mode", True)
