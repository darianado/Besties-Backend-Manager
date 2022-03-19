from auth_seeder import AuthSeeder
import uuid

from auth_seeder import Generator


class Seeder:

  def __init__(self, settings):
    self.settings = settings
    generator = Generator()
    self.auth_seeder = AuthSeeder(generator)

  def _generate_uids(self, amount):
    return [uuid.uuid4().hex for _ in range(amount)]

  def seed(self):
    uids = self._generate_uids(self.settings.seeding.number_of_users_to_seed)

    print(f"Seeding {len(uids)} users.")
    self.auth_seeder.seed(uids, self.settings.seeding.email_verified, self.settings.seeding.password)

  def unseed(self):
    self.auth_seeder.unseed()