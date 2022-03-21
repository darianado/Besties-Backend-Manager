import glob
import random

import pytz
from faker import Faker
from firebase_admin import firestore

from models import AgeSpan, CategorizedInterests, Category, Context


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
