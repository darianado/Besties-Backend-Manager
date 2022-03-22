import uuid
from typing import List

from alive_progress import alive_bar

from abstracts import SeedableService
from constants import CIRCLES_BAR, CIRCLES_BAR_SPINNER
from decorators import safe_exit, sleepy_exit
from enums import RunMode
from environment_manager import EnvironmentManager
from generator import Generator
from services.services_manager import ServicesManager
from utils import load_settings
import requests, json, time


class Functions():
  def __init__(self, environment_manager: EnvironmentManager, services_manager: ServicesManager):
    self.services_manager = services_manager
    self.matching_handler = MatchingHandler(environment_manager)
    self.recommendation_handler = RecommendationHandler(environment_manager)
    self.seeder = Seeder()
    self.environment_manager = environment_manager

  @sleepy_exit
  @safe_exit
  def seed(self):
    services = self.services_manager.get_seedable_services()
    self.seeder.seed(services)

  @sleepy_exit
  @safe_exit
  def unseed(self):
    services = self.services_manager.get_seedable_services()
    self.seeder.unseed(services)

  @safe_exit
  def get_recommendations(self):
    self.recommendation_handler.get_recommendations()

  @safe_exit
  def like_user(self):
    self.matching_handler.like_user()

class MatchingHandler:
  def __init__(self, environment_manager: EnvironmentManager):
    self.environment_manager = environment_manager
    self.reload_settings()

  def reload_settings(self):
    self.settings = load_settings()

  def like_user(self):
    self.reload_settings()

    run_mode = self.environment_manager.run_mode
    matching_settings = self.settings["matching"]
    url = matching_settings["emulator_url"] if run_mode == RunMode.EMULATOR else matching_settings["production_url"]
    print(url)

    payload = {
      "likerUserID": input("Type the user ID of the person liking: "),
      "likeeUserID": input("Type the user ID of the person being liked: ")
    }

    start_time = time.time()
    response = requests.post(url, json=payload)
    unwrapped_response = json.loads(response.text)

    print("\nReceived the following in %.2f seconds:\n" % (time.time() - start_time))
    print(unwrapped_response)
    print("")

    input("Press enter to go back... ")

class RecommendationHandler:
  def __init__(self, environment_manager: EnvironmentManager):
    self.environment_manager = environment_manager
    self.reload_settings()

  def reload_settings(self):
    self.settings = load_settings()

  def get_recommendations(self):
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

class Seeder:
  def __init__(self):
    self.reload_settings()

  def _generate_uids(self, amount):
    return [uuid.uuid4().hex for _ in range(amount)]

  def reload_settings(self):
    self.settings = load_settings()

  def seed(self, services: List[SeedableService]):
    self.reload_settings()

    generator = Generator(self.settings)
    number_of_users_to_seed = self.settings["seeding"]["number_of_users_to_seed"]
    uids = self._generate_uids(number_of_users_to_seed)

    print(f"Seeding {number_of_users_to_seed} users.")
    print("")

    for service in services:
      with alive_bar(number_of_users_to_seed, title=service.twenty_char_name() + ":", bar=CIRCLES_BAR) as bar:
        service.seed(uids, generator, bar)

    print("")
    print("Successfully seeded to all services.")

  def unseed(self, services: List[SeedableService]):
    print("Unseeding users.")
    print("")

    for service in services:
      with alive_bar(title=service.twenty_char_name() + ":", bar=CIRCLES_BAR, unknown=CIRCLES_BAR_SPINNER) as bar:
        service.unseed(bar)

    print("")
    print("Successfully unseeded all services.")
