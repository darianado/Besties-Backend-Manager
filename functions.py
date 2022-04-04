from decorators import safe_exit, sleepy_exit
from environment_manager import EnvironmentManager
from handlers.matching_handler import MatchingHandler
from handlers.recommendation_handler import RecommendationHandler
from handlers.seeding_handler import SeedingHandler
from services.services_manager import ServicesManager


class Functions():
  """Class containing the first-step functions called directly from various menu 
  items on various screens. Each method typically utilizes handler classes to handle the bulk of the work."""

  def __init__(self, environment_manager: EnvironmentManager, services_manager: ServicesManager):
    self.services_manager = services_manager
    self.matching_handler = MatchingHandler(environment_manager)
    self.recommendation_handler = RecommendationHandler(environment_manager)
    self.seeder = SeedingHandler()
    self.environment_manager = environment_manager

  @sleepy_exit
  @safe_exit
  def seed(self):
    """First-step function when selecting the seed element from the menu."""
    services = self.services_manager.get_seeding_services()
    self.seeder.seed(services)

  @sleepy_exit
  @safe_exit
  def unseed(self):
    """First-step function when selecting the unseed element from the menu."""
    services = self.services_manager.get_unseeding_services()
    self.seeder.unseed(services)

  @safe_exit
  def get_recommendations(self):
    """First-step function when selecting the element to get recommendations for a given user."""
    self.recommendation_handler.get_recommendations()

  @sleepy_exit
  @safe_exit
  def like_user(self):
    """First-step function when liking a given user."""
    self.matching_handler.like_user_ask_input()
