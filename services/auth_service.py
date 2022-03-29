from typing import List

from abstracts import SeedableService
from constants import AUTH_RUN_MODES
from enums import RunMode
from firebase_admin import auth
from generator import Generator


class AuthService(SeedableService):

  def __init__(self, settings):
    self.settings = settings

  def is_active_in(cls, run_mode: RunMode) -> bool:
    return (run_mode in AUTH_RUN_MODES)

  @classmethod
  def name(cls):
    return "Authentication"

  def can_seed(self):
    return True

  def can_unseed(self):
    return self.settings["seeding"]["auth_should_unseed"]

  def amount_to_seed(self, uids: List[str]) -> int:
    return len(uids)

  def seed(self, uids: List[str], required_accounts, generator: Generator, progress_callback):
    super().seed(uids, generator, required_accounts, progress_callback)


    number_of_required_accounts = len(required_accounts)
    required_accounts_uids = uids[:number_of_required_accounts]
    random_accounts_uids = uids[number_of_required_accounts:]

    for required_account in required_accounts:
      uid = required_accounts_uids.pop()
      email = required_account["email"]
      password = required_account["password"]

      auth.create_user(
        uid=uid,
        email=email,
        email_verified=self.settings["seeding"]["context"]["email_verified"],
        password=password)

      progress_callback()

    for uid in random_accounts_uids:
      auth.create_user(
        uid=uid,
        email=generator.pick_unique_email(),
        email_verified=self.settings["seeding"]["context"]["email_verified"],
        password=self.settings["seeding"]["context"]["password"])

      progress_callback()

  def unseed(self, progress_callback):
    super().unseed(progress_callback)

    for user in auth.list_users().iterate_all():
      auth.delete_user(user.uid)
      progress_callback()
