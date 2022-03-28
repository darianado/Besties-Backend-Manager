import uuid
from typing import List

from alive_progress import alive_bar

from abstracts import SeedableService
from constants import CIRCLES_BAR, CIRCLES_BAR_SPINNER
from generator import Generator
from utils import load_settings


class SeedingHandler:
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
      total = service.amount_to_seed(uids)
      with alive_bar(total, title=service.twenty_char_name() + ":", bar=CIRCLES_BAR) as bar:
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
