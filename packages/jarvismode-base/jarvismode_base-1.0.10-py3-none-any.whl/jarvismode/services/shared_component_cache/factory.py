from typing import TYPE_CHECKING

from typing_extensions import override

from jarvismode.services.factory import ServiceFactory
from jarvismode.services.shared_component_cache.service import SharedComponentCacheService

if TYPE_CHECKING:
    from jarvismode.services.settings.service import SettingsService


class SharedComponentCacheServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(SharedComponentCacheService)

    @override
    def create(self, settings_service: "SettingsService"):
        return SharedComponentCacheService(expiration_time=settings_service.settings.cache_expire)
