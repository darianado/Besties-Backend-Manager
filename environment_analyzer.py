import os
import platform
from colors import color

from constants import FIRESTORE_EMULATOR_ENVIRONMENT_VARIABLE
from enums import Platform, RunMode


class EnvironmentAnalyzer:
  def __init__(self):
    self.platform_type = self.analyze_platform()
    self.run_mode = self.analyze_run_mode()

  def analyze_platform(self):
    platform_type = platform.system()

    if(platform_type == "Windows"):
      return Platform.WINDOWS
    elif(platform_type == "Darwin"):
      return Platform.MACOS
    else:
      return platform_type

  def analyze_run_mode(self):
    env_var_set = os.environ.get(FIRESTORE_EMULATOR_ENVIRONMENT_VARIABLE) is not None

    if(env_var_set):
      return RunMode.EMULATOR
    else:
      return RunMode.PRODUCTION

  def _get_os_environment_description(self):
    if(self.platform_type == Platform.WINDOWS or self.platform_type == Platform.MACOS):
      return color("[✔]", fg="green") + f" {self.platform_type.value} is supported."
    else:
      return color("[✘]", fg="red") + f" {self.platform_type} is not supported."


  def _get_run_mode_description(self):
    if(self.run_mode == RunMode.EMULATOR):
      return color("[✔]", fg="green") + """ Emulator mode. 
                                      \n    Switch to production mode:
                                      \n     • Exit this app
                                      \n     • Restart your terminal
                                      \n     • Restart this app"""
    elif(self.run_mode == RunMode.PRODUCTION):
      return color("[!]", fg="orange") + f""" Production mode. 
                                        \n    {color("BE CAREFUL; YOU ARE ALTERING THE PRODUCTION ENVIRONMENT!", fg="red")} 
                                        \n    Switch to emulator mode:
                                        \n     • Exit this app
                                        \n     • Run this command: 
                                        \n           export FIRESTORE_EMULATOR_HOST=\"localhost:8080\"
                                        \n     • Restart this app"""
    else:
      return color("[✘]", fg="red") + " Error: Unrecognizable run mode."


  def get_available_features_description(self):
    result = "Active features:\n"

    if(self.run_mode == RunMode.EMULATOR):
      return result + f"""{color("[✔]", fg="green")} Firestore
                        \n{color("[✔]", fg="green")} Functions
                        \n{color("[✘]", fg="red")} Storage (Not available for Python Admin SDK)"""
    elif(self.run_mode == RunMode.PRODUCTION):
      return result + f"""{color("[✔]", fg="green")} Firestore
                        \n{color("[✔]", fg="green")} Functions
                        \n{color("[✔]", fg="green")} Storage"""
    else:
      return color("[✘]", fg="red") + " Error: Unrecognizable run mode."


  def get_environment_description(self):
    result = "Your environment:\n"
    result += self._get_os_environment_description()
    result += "\n"
    result += self._get_run_mode_description()
    return result

  def get_command_for_opening_file_in_environment(self, filename):
    if(self.platform_type == Platform.WINDOWS):
      return f"code {filename}"
    elif(self.platform_type == Platform.MACOS):
      return f"open -a 'Visual Studio Code.app' {filename}"
    else:
      return f"open {filename}"
