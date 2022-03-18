import json
import datetime
from typing import Dict, List
import pytz
from abc import ABC, abstractmethod

from constants import SETTINGS_FILENAME


class ConstructableFromDict(ABC):
  @classmethod
  @abstractmethod
  def from_dict(cls, dict: Dict[str, any]):
    pass


class ListConstructableFromDict(ABC):
  @classmethod
  @abstractmethod
  def from_list_of_dicts(cls, list: List[Dict[str, any]]):
    pass


class AgeSpan(ConstructableFromDict):
  def __init__(self, from_date: datetime, to_date: datetime):
    self.from_date = (from_date,)
    self.to_date = to_date

  @classmethod
  def from_dict(cls, dict: Dict[str, any]):
    age_from = dict["from"]
    age_to = dict["to"]

    age_from_date = datetime.datetime(age_from["year"], age_from["month"], age_from["day"], tzinfo=pytz.UTC)
    age_to_date = datetime.datetime(age_to["year"], age_to["month"], age_to["day"], tzinfo=pytz.UTC)

    return cls(age_from_date,
               age_to_date)


class InterestCategory(ConstructableFromDict, ListConstructableFromDict):
  def __init__(self, title: str, entries: List[str]):
    self.title = title
    self.entries = entries

  @classmethod
  def from_dict(cls, dict: Dict[str, any]):
    return cls(dict["title"], dict["entries"])

  @classmethod
  def from_list_of_dicts(cls, list: List[Dict[str, any]]):
    return [cls.from_dict(entry) for entry in list]


class AppContext(ConstructableFromDict):
  def __init__(self,
               genders: List[str],
               relationship_statuses: List[str],
               categorized_interests: List[InterestCategory],
               universities: List[str]):
    self.genders = genders
    self.relationship_statuses = relationship_statuses
    self.categorized_interests = categorized_interests
    self.universities = universities

  @classmethod
  def from_dict(cls, dict: Dict[str, any]):
    categorized_interests = InterestCategory.from_list_of_dicts(dict["categorized_interests"])

    return cls(dict["genders"],
               dict["relationship_statuses"],
               categorized_interests,
               dict["universities"])


class SeedSettings(ConstructableFromDict):
  def __init__(self,
               number_of_users_to_seed: int,
               profile_image_folder: str,
               age_span: AgeSpan,
               use_global_context: bool,
               local_context: AppContext):
    self.number_of_users_to_seed = number_of_users_to_seed
    self.profile_image_folder = profile_image_folder
    self.age_span = age_span
    self.use_global_context = use_global_context
    self.local_context = local_context

  @classmethod
  def from_dict(cls, dict: Dict[str, any]):
    age_span = AgeSpan.from_dict(dict["age_span"])
    local_context = AppContext.from_dict(dict["local_context"])

    return cls(dict["number_of_users_to_seed"],
               dict["profile_image_folder"],
               age_span,
               dict["use_global_context"],
               local_context)


class RecommendationSettings(ConstructableFromDict):
  def __init__(self,
               emulator_rec_url: str,
               production_rec_url: str,
               number_of_recommendations_to_request: str):
    self.emulator_rec_url = emulator_rec_url
    self.production_rec_url = production_rec_url
    self.number_of_recommendations_to_request = number_of_recommendations_to_request

  @classmethod
  def from_dict(cls, dict: Dict[str, any]):
    return cls(dict["emulator_rec_url"],
               dict["production_rec_url"],
               dict["number_of_recommendations_to_request"])


class Settings(ConstructableFromDict):
  def __init__(self,
               seed_settings: SeedSettings,
               recommendation_settings: RecommendationSettings):
    self.seed_settings = seed_settings
    self.recommendation_settings = recommendation_settings

  @classmethod
  def from_dict(cls, dict: Dict[str, any]):
    seed_settings = SeedSettings.from_dict(dict["seeding"])
    recommendation_settings = RecommendationSettings.from_dict(dict["recommendations"])

    return cls(seed_settings, recommendation_settings)


class SettingsReader:
  def __init__(self):
    dict = self._load()

    ic = Settings.from_dict(dict)

  def _load(self) -> Dict[str, any]:
    try:
      return json.load(open(SETTINGS_FILENAME))
    except:
      print(
        f"""ERROR: Could not load settings file. 
      Please check that a file by the name \'{SETTINGS_FILENAME}\' exists, 
      and contains properly formatted json."""
      )
