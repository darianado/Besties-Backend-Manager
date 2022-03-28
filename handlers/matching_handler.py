from environment_manager import EnvironmentManager
from utils import load_settings
import requests, json, time
from enums import RunMode

class MatchingHandler:
  def __init__(self, environment_manager: EnvironmentManager):
    self.environment_manager = environment_manager
    self.reload_settings()

  def reload_settings(self):
    self.settings = load_settings()

  def like_user(self):
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
    self.reload_settings()

    run_mode = self.environment_manager.run_mode
    matching_settings = self.settings["matching"]
    url = matching_settings["emulator_url"] if run_mode == RunMode.EMULATOR else matching_settings["production_url"]

    payload = {
      "likerUserID": uidOne,
      "otherUserID": uidTwo
    }
    return requests.post(url, json=payload)
