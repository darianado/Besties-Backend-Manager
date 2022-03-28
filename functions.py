from decorators import safe_exit, sleepy_exit
from environment_manager import EnvironmentManager
from handlers.matching_handler import MatchingHandler
from handlers.recommendation_handler import RecommendationHandler
from handlers.seeding_handler import SeedingHandler
from services.services_manager import ServicesManager


class Functions():
  def __init__(self, environment_manager: EnvironmentManager, services_manager: ServicesManager):
    self.services_manager = services_manager
    self.matching_handler = MatchingHandler(environment_manager)
    self.recommendation_handler = RecommendationHandler(environment_manager)
    self.seeder = SeedingHandler()
    self.environment_manager = environment_manager

  @sleepy_exit
  @safe_exit
  def seed(self):
    services = self.services_manager.get_seeding_services()
    self.seeder.seed(services)

  @sleepy_exit
  @safe_exit
  def unseed(self):
    services = self.services_manager.get_unseeding_services()
    self.seeder.unseed(services)

  @safe_exit
  def get_recommendations(self):
    self.recommendation_handler.get_recommendations()

  @safe_exit
  def like_user(self):
    self.matching_handler.like_user()
