import json
import random
import faker

class Generator():

    def __init__(self, settings):
        file = json.load(open(settings))

        self.fake = faker.Faker()

        self.number = file['number']
        self.age_span = file['age_span']
        self.genders = file['genders']
        self.location_span = file['location_span']
        self.categories = file['categories']

    def _pick_age(self):
        return random.randint(self.age_span['from'], self.age_span['to'])

    def _pick_location(self):
        return {
            "lat": random.uniform(self.location_span['lat0'], self.location_span['lat1']),
            "lon": random.uniform(self.location_span['lon0'], self.location_span['lon1'])
        }

    def _pick_gender(self):
        return self.genders[random.randint(0, len(self.genders) - 1)]

    def _pick_interests(self):
        picked = []
        for category in self.categories:
            values = self.categories[category]

            number_to_pick = random.randint(0, len(values) - 1)
            picked += random.sample(values, k=number_to_pick)
        return picked


    def generate_user(self):
        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "age": self._pick_age(),
            "gender": self._pick_gender(),
            "location": self._pick_location(),
            "interests": self._pick_interests(),
            "preferences": self._pick_interests()
        }

    def generate(self):
        users = []
        for _ in range(self.number):
            users.append(self.generate_user())
        return users