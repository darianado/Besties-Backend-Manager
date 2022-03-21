from typing import List

from abstracts import Seedable, Service
from colors import color
from environment_manager import EnvironmentManager
from utils import load_settings

from services.auth_service import AuthService
from services.firestore_service import FirestoreService
from services.storage_service import StorageService


class ServicesManager:

  services: List[Service] = []
  
  def __init__(self, environment_manager: EnvironmentManager):
    self.settings = load_settings()
    self.environment_manager = environment_manager
    self._initialize_services(self.settings)

  def _initialize_services(self, settings):
    self.services.append(AuthService(settings))
    self.services.append(FirestoreService(settings))
    self.services.append(StorageService(settings))

  def _get_active_services(self):
    run_mode = self.environment_manager.run_mode
    result = []

    for service in self.services:
      if service.is_active_in(run_mode): result.append(service)

    return result

  def get_seedable_services(self) -> List[Seedable]:
    active = self._get_active_services()
    result = []

    for service in active:
      if issubclass(type(service), Seedable): result.append(service)

    return result

  def get_available_features_description(self):
    run_mode = self.environment_manager.run_mode
    result = "Active services:\n"

    for service in self.services:
      result += (color("[✔]", fg="green") if(service.is_active_in(run_mode)) else color("[✘]", fg="red")) + " " + service.name() + "\n"

    return result
