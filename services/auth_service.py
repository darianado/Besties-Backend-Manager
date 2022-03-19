from abc import ABC, abstractmethod
from random import seed
from typing import List
from faker import Faker
from firebase_admin import auth, firestore
import pytz
from constants import AUTH_RUN_MODES, FIRESTORE_BATCH_SIZE, FIRESTORE_RUN_MODES, STORAGE_RUN_MODES
import datetime
from enums import RunMode


class Generator:
  def __init__(self, settings):
    self.faker = Faker()
    self._setup_context(settings)

  def _setup_context(self, settings):
    should_use_global_context = settings.seeding.use_global_context
    if(not should_use_global_context):
      self.context = settings.local_context
    else:
      global_context_doc_path = settings.seeding.global_context_doc_path
      doc = firestore.client().document(global_context_doc_path).get()
      self.context = doc.to_dict()

  def _pick_dob(self):
    age_from_date = datetime.datetime(age_from['year'], age_from['month'], age_from['day'], tzinfo=pytz.UTC)
    return self.fake.date_time_between(start_date=self.age_from_date, end_date=self.age_to_date, tzinfo=pytz.UTC)

  def generate_unique_email(self):
    return self.faker.unique.email()

  def generate_user_data():
    
    return {
      "test": "test"
    }


class Service(ABC):

  @abstractmethod
  def is_active_in(cls, run_mode: RunMode) -> bool:
    pass

  @classmethod
  @abstractmethod
  def name(cls):
    pass

  @classmethod
  def twenty_char_name(cls):
    name = cls.name()
    return " " * (20 - len(name)) + name

class Seedable(ABC):
  @abstractmethod
  def seed(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    pass

  @abstractmethod
  def unseed(self, progress_callback) -> List[str]:
    pass


class SeedableService(Service, Seedable):
  pass


class AuthService(SeedableService):

  def __init__(self, settings):
    self.settings = settings

  def is_active_in(cls, run_mode: RunMode) -> bool:
    return (run_mode in AUTH_RUN_MODES)

  @classmethod
  def name(cls):
    return "Authentication"

  def seed(self, uids: List[str], generator: Generator, progress_callback):
    super().seed(uids, generator, progress_callback)

    for uid in uids:
      auth.create_user(
        uid=uid,
        email=generator.generate_unique_email(),
        email_verified=self.settings.seeding.email_verified,
        password=self.settings.seeding.password)

      progress_callback()

  def unseed(self, progress_callback):
    super().unseed(progress_callback)

    for user in auth.list_users().iterate_all():
      auth.delete_user(user.uid)
      progress_callback()


class FirestoreService(SeedableService):
  def __init__(self, settings):
    self.settings = settings
    self.db = firestore.client()

  def is_active_in(cls, run_mode: RunMode) -> bool:
    return (run_mode in FIRESTORE_RUN_MODES)

  @classmethod
  def name(cls):
    return "Firestore"

  def seed(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    super().seed(uids, generator, progress_callback)

    users_collection_ref = self.settings.seeding.firestore_users_collection_path

    for uid in uids:
      data = generator.generate_user_data()
      self.db.collection(users_collection_ref).document(uid).set(data)
      progress_callback()

  def unseed(self, progress_callback) -> List[str]:
    super().unseed(progress_callback)

    users_collection_ref = self.settings.seeding.firestore_users_collection_path
    docs = self.db.collection(users_collection_ref).limit(FIRESTORE_BATCH_SIZE).stream()
    deleted = 0

    for doc in docs:
      doc.reference.delete()
      deleted = deleted + 1
      progress_callback()

    if deleted >= self.BATCH_SIZE:
      return self.unseed(progress_callback)


class StorageService(SeedableService):

  def __init__(self, settings):
    self.settings = settings

  def is_active_in(cls, run_mode: RunMode) -> bool:
    return (run_mode in STORAGE_RUN_MODES)

  @classmethod
  def name(cls):
    return "Storage"

  def seed(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    return super().seed(uids, generator, progress_callback)

  def unseed(self, progress_callback) -> List[str]:
    return super().unseed(progress_callback)
