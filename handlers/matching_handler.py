from environment_manager import EnvironmentManager
from utils import load_settings
import requests, json, time
from enums import RunMode

class MatchingHandler:
  """Class that handles communication with the backend for
  matchmaking-related functions."""

  def __init__(self, environment_manager: EnvironmentManager):
    self.environment_manager = environment_manager
    self.reload_settings()

  def reload_settings(self):
    """Reloads the settings file to get newest changes."""
    self.settings = load_settings()

  def like_user(self):
    """Queries the user to input two user IDs sequentially, where the first indicates 
    the user doing the liking, and the second indicates the user being liked. 
    It then forwards this request to the backend, and prints it out."""
    uidOne = input("Type the user ID of the person liking: ")
    uidTwo = input("Type the user ID of the person being liked: ")

    start_time = time.time()
    response = self.like_user(uidOne, uidTwo)
    unwrapped_response = json.loads(response.text)

    print("\nReceived the following in %.2f seconds:\n" % (time.time() - start_time))
    print(unwrapped_response)
    print("")

    input("Press enter to go back... ")


  def like_user(self, uidOne: str, uidTwo: str):
    """Requests that the user indicated by uidOne likes the user indicated by uidTwo from the backend."""
    self.reload_settings()

    run_mode = self.environment_manager.run_mode
    matching_settings = self.settings["matching"]
    url = matching_settings["emulator_url"] if run_mode == RunMode.EMULATOR else matching_settings["production_url"]

    payload = {
      "likerUserID": uidOne,
      "otherUserID": uidTwo
    }
    return requests.post(url, json=payload)
