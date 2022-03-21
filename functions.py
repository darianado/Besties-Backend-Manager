import uuid
from typing import List

from alive_progress import alive_bar

from abstracts import SeedableService
from constants import CIRCLES_BAR, CIRCLES_BAR_SPINNER
from decorators import safe_exit, sleepy_exit
from generator import Generator
from services.services_manager import ServicesManager
from utils import load_settings


class Functions():
  def __init__(self, services_manager: ServicesManager):
    self.services_manager = services_manager
    self.seeder = Seeder()

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

  @sleepy_exit
  @safe_exit
  def get_recommendations(self):
    pass


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
