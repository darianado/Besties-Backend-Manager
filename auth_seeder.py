from faker import Faker
from firebase_admin import auth, exceptions
import hmac
import hashlib
import base64

class Generator:
  def __init__(self):
    self.faker = Faker()

  def generate_unique_email(self):
    return self.faker.unique.email()



class AuthSeeder:
  def __init__(self, generator: Generator):
    self.generator = generator

  def seed(self, uids, email_verified, password):
    for uid in uids:
      auth.create_user(
        uid=uid,
        email=self.generator.generate_unique_email(),
        email_verified=email_verified,
        password=password
      )

  def unseed(self):
    for user in auth.list_users().iterate_all():
      auth.delete_user(user.uid)
