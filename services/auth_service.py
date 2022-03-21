from abc import ABC, abstractmethod
import glob
from random import seed
from typing import List
from faker import Faker
from firebase_admin import auth, firestore, storage
from numpy import double
import pytz
from constants import AUTH_RUN_MODES, FIRESTORE_BATCH_SIZE, FIRESTORE_RUN_MODES, STORAGE_RUN_MODES
import datetime
from enums import RunMode
import random
from io import BytesIO

class AgeSpan:
  def __init__(self, from_date: datetime, to_date: datetime):
    self.from_date = from_date
    self.to_date = to_date

  @classmethod
  def from_dict(cls, dict):
    age_from = dict["from"]
    age_to = dict["to"]

    age_from_date = datetime.datetime(age_from['year'], age_from['month'], age_from['day'], tzinfo=pytz.UTC)
    age_to_date = datetime.datetime(age_to['year'], age_to['month'], age_to['day'], tzinfo=pytz.UTC)

    return AgeSpan(age_from_date, age_to_date)


class Category:
  def __init__(self, title: str, interests: List[str]):
    self.title = title
    self.interests = interests

  @classmethod
  def from_dict(cls, dict):
    return Category(dict['title'], dict['entries'])

  def to_dict(self):
    return {
      "title": self.title,
      "interests": self.interests
    }


class CategorizedInterests:
  def __init__(self, categories: List[Category]):
    self.categories = categories

  @classmethod
  def from_list(cls, list):
    categories = [Category.from_dict(entry) for entry in list]
    return CategorizedInterests(categories=categories)

  def to_list(self):
    return [e.to_dict() for e in self.categories]


class Context:
  def __init__(self,
               age_span: AgeSpan,
               genders: List[str],
               categorized_interests: CategorizedInterests,
               universities: List[str],
               relationship_statuses: List[str]):
    self.age_span = age_span
    self.genders = genders
    self.categorized_interests = categorized_interests
    self.universities = universities
    self.relationship_statuses = relationship_statuses


class Generator:

  def __init__(self, settings):
    self.db = firestore.client()
    self.faker = Faker()
    self.settings = settings
    self.context = self._read_context(settings)

  def _read_context(self, settings):
    context = settings["seeding"]["context"]

    age_span = AgeSpan.from_dict(context["age_span"])
    genders = context["genders"]
    relationship_statuses = context["relationship_statuses"]
    categorized_interests = CategorizedInterests.from_list(context["categorized_interests"])
    universities = context["universities"]

    return Context(age_span=age_span,
                   genders=genders,
                   categorized_interests=categorized_interests,
                   universities=universities,
                   relationship_statuses=relationship_statuses)

  def pick_dob(self):
    from_date = self.context.age_span.from_date
    to_date = self.context.age_span.to_date

    return self.faker.date_time_between(start_date=from_date, end_date=to_date, tzinfo=pytz.UTC)

  def pick_gender(self):
    genders = self.context.genders
    return genders[random.randint(0, len(genders) - 1)]

  def pick_relationship_status(self):
    relationship_statuses = self.context.relationship_statuses
    return relationship_statuses[random.randint(0, len(relationship_statuses) - 1)]

  def pick_university(self):
    universities = self.context.universities
    return universities[random.randint(0, len(universities) - 1)]

  def pick_interests(self):
    categories = self.context.categorized_interests.categories
    number_to_pick = random.randint(self.settings["seeding"]["min_interests_to_pick"], self.settings["seeding"]["max_interests_to_pick"])

    picked_categories = []

    for (i, category) in enumerate(categories):

      if not i == len(categories) - 1:
        number_to_pick_from_this_category = random.randint(0, number_to_pick)
        number_to_pick -= number_to_pick_from_this_category
      else:
        number_to_pick_from_this_category = number_to_pick

      picked_interests = random.sample(category.interests, k=min(number_to_pick_from_this_category, len(category.interests)))
      picked_categories.append(Category(category.title, interests=picked_interests))

    return CategorizedInterests(picked_categories)


  def pick_photo(self):
    files = glob.glob(self.settings["seeding"]["profile_image_folder"] + "*.jpg")
    return random.choice(files)

  def pick_unique_email(self):
    return self.faker.unique.email()

  def generate_bio(self):
    max_bio_length = self.settings["seeding"]["max_bio_length"]
    return self.faker.text(max_nb_chars=max_bio_length)

  def generate_user_data(self):
    return {
      "bio": self.generate_bio(),
      "dob": self.pick_dob(),
      "firstName": self.faker.first_name(),
      "lastName": self.faker.last_name(),
      "gender": self.pick_gender(),
      "relationshipStatus": self.pick_relationship_status(),
      "university": self.pick_university(),
      "categorizedInterests": self.pick_interests().to_list(),
      "preferences": {
        "categorizedInterests": self.pick_interests().to_list(),
        "maxAge": 50,
        "minAge": 18
      }
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
        email=generator.pick_unique_email(),
        email_verified=self.settings["seeding"]["context"]["email_verified"],
        password=self.settings["seeding"]["context"]["password"])

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
    users_collection_ref = self.settings["seeding"]["firestore_users_collection_path"]
    user_data_ref = self.db.collection(users_collection_ref)
    split_size = min(FIRESTORE_BATCH_SIZE, len(uids))

    for split in [uids[i:i + split_size] for i in range(0, len(uids), split_size)]:
      batch = self.db.batch()

      for uid in split:
        data = generator.generate_user_data()
        batch.set(user_data_ref.document(uid), data)
        progress_callback()

      batch.commit()

  def unseed(self, progress_callback) -> List[str]:
    super().unseed(progress_callback)

    users_collection_ref = self.settings["seeding"]["firestore_users_collection_path"]
    docs = self.db.collection(users_collection_ref).limit(FIRESTORE_BATCH_SIZE).stream()
    deleted = 0

    for doc in docs:
      doc.reference.delete()
      deleted = deleted + 1
      progress_callback()

    if deleted >= FIRESTORE_BATCH_SIZE:
      return self.unseed(progress_callback)


class StorageService(SeedableService):

  def __init__(self, settings):
    self.settings = settings
    self.bucket = storage.bucket()

  def is_active_in(cls, run_mode: RunMode) -> bool:
    return (run_mode in STORAGE_RUN_MODES)

  @classmethod
  def name(cls):
    return "Storage"

  def _save_url_to_user(self, uid, url):
    users_collection_ref = self.settings["seeding"]["firestore_users_collection_path"]
    firestore.client().collection(users_collection_ref).document(uid).set({
      "profileImageUrl": url
    }, merge=True)

  def seed(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    storage_profile_image_folder = self.settings["seeding"]["storage_profile_image_folder"]

    for uid in uids:
      local_file_path = generator.pick_photo()
      blob = self.bucket.blob(storage_profile_image_folder + uid + ".jpg")
      blob.content_type = "image/jpeg"

      with open(local_file_path, "rb") as file:
        blob.upload_from_file(file)
        
      blob.make_public()
      self._save_url_to_user(uid, blob.public_url)

      progress_callback()


  def unseed(self, progress_callback) -> List[str]:
    storage_profile_image_folder = self.settings["seeding"]["storage_profile_image_folder"]
    blobs = self.bucket.list_blobs(prefix=storage_profile_image_folder)

    for blob in blobs:
      blob.delete()
      progress_callback()
