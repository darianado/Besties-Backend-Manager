import json
import os, glob
import random
import uuid, pytz
import faker, datetime

class Generator():

    def __init__(self, settings):
        file = json.load(open(settings))

        self.fake = faker.Faker()

        self.image_folder = file['image_folder']
        self.number = file['number']
        self.age_span = file['age_span']
        self.genders = file['genders']
        self.location_span = file['location_span']
        self.categories = file['categories']
        self.universities = file['universities']
        self.relationshipStatuses = file['relationshipStatuses']


        age_from = self.age_span['from']
        age_to = self.age_span['to']

        self.age_from_date = datetime.datetime(age_from['year'], age_from['month'], age_from['day'], tzinfo=pytz.UTC)
        self.age_to_date = datetime.datetime(age_to['year'], age_to['month'], age_to['day'], tzinfo=pytz.UTC)

    def _pick_dob(self):
      return self.fake.date_time_between(start_date=self.age_from_date, end_date=self.age_to_date, tzinfo=pytz.UTC)

    def _pick_location(self):
      return {
        "lat": random.uniform(self.location_span['lat0'], self.location_span['lat1']),
        "lon": random.uniform(self.location_span['lon0'], self.location_span['lon1'])
      }

    def _pick_gender(self):
        return self.genders[random.randint(0, len(self.genders) - 1)]

    def _pick_relationship_status(self):
      return self.relationshipStatuses[random.randint(0, len(self.relationshipStatuses) - 1)]

    def _pick_interests(self):
        picked = []
        for category in self.categories:
            values = self.categories[category]

            number_to_pick = random.randint(0, len(values) - 1)
            picked += random.sample(values, k=number_to_pick)
        return picked


    def _pick_photos(self):
      files = glob.glob(self.image_folder + "*.jpg")
      return [random.choice(files)]

    def _pick_university(self):
      index = random.randint(0, len(self.universities) - 1)
      return self.universities[index]


    def generate_user(self):
      return {
        "uid": uuid.uuid4().hex,
        "images": self._pick_photos(),
        "firstName": self.fake.first_name(),
        "lastName": self.fake.last_name(),
        "dob": self._pick_dob(),
        "gender": self._pick_gender(),
        "location": self._pick_location(),
        "interests": self._pick_interests(),
        "university": self._pick_university(),
        "bio": self.fake.paragraph(nb_sentences=2),
        "relationshipStatus": self._pick_relationship_status(),
        "preferences": {
          "interests": self._pick_interests(),
          "maxAge": self.age_to_date,
          "minAge": self.age_from_date
        }
      }

    def generate(self):
        users = []
        for _ in range(self.number):
            users.append(self.generate_user())
        return users