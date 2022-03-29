from environment_manager import EnvironmentManager
from utils import load_settings
import requests, json, time
from enums import RunMode

class RecommendationHandler:
  """Class that handles communication with the backend for
  recommendation-related functions."""

  def __init__(self, environment_manager: EnvironmentManager):
    self.environment_manager = environment_manager
    self.reload_settings()

  def reload_settings(self):
    """Reloads the settings file to get newest changes."""
    self.settings = load_settings()

  def get_recommendations(self):
    """Queries the user to input a user ID for which to get recommendations. 
    Then forwards this request to the backend, and prints it out."""
    self.reload_settings()

    run_mode = self.environment_manager.run_mode
    recommendation_settings = self.settings["recommendations"]
    rec_url = recommendation_settings["emulator_rec_url"] if run_mode == RunMode.EMULATOR else recommendation_settings["production_rec_url"]

    payload = {
      "uid": input("Type a user ID: "),
      "recs": recommendation_settings["number_of_recommendations_to_request"]
    }

    start_time = time.time()
    response = requests.post(rec_url, json=payload)
    unwrapped_response = json.loads(response.text)

    print("\nReceived the following in %.2f seconds:\n" % (time.time() - start_time))
    print(unwrapped_response)
    print("")

    input("Press enter to go back... ")