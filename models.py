import datetime
from typing import List

import pytz


class AgeSpan:
  """Representation of an age span. Used in generating dates within a span."""

  def __init__(self, from_date: datetime, to_date: datetime):
    self.from_date = from_date
    self.to_date = to_date

  @classmethod
  def from_dict(cls, dict):
    """Returns a representation of the provided dictionary as an AgeSpan object."""
    age_from = dict["from"]
    age_to = dict["to"]

    age_from_date = datetime.datetime(age_from['year'], age_from['month'], age_from['day'], tzinfo=pytz.UTC)
    age_to_date = datetime.datetime(age_to['year'], age_to['month'], age_to['day'], tzinfo=pytz.UTC)

    return AgeSpan(age_from_date, age_to_date)


class Category:
  """Representation of a category of interests. Contains a list of interests within it, as well as a title."""

  def __init__(self, title: str, interests: List[str]):
    self.title = title
    self.interests = interests

  @classmethod
  def from_dict(cls, dict):
    """Returns a representation of the provided dictionary as a Category object."""
    return Category(dict['title'], dict['entries'])

  def to_dict(self):
    """Returns a representation of this object as a dictionary."""
    return {
      "title": self.title,
      "interests": self.interests
    }


class CategorizedInterests:
  """Representation of categorized interests. Contains a list of categories within it."""

  def __init__(self, categories: List[Category]):
    self.categories = categories

  @classmethod
  def from_list(cls, list):
    """Returns a representation of the provided list as a CategorizedInterests object."""
    categories = [Category.from_dict(entry) for entry in list]
    return CategorizedInterests(categories=categories)

  def to_list(self):
    """Returns a representation of this object as a list."""
    return [e.to_dict() for e in self.categories]


class Context:
  """Representation of a 'seeding context', i.e. general parameters used for seeding users."""

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
