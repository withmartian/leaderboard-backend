import inspect
import sys

from providers.abstract_providers import BaseProvider
from providers.concrete_providers import *


class ProviderFactory:
    @staticmethod
    def _create_provider_classes() -> dict[str, type[BaseProvider]]:
        providers_classes = {}
        for _, obj in inspect.getmembers(sys.modules["providers.concrete_providers"]):
            if inspect.isclass(obj) and issubclass(obj, BaseProvider):
                providers_classes[obj.NAME] = obj
        return providers_classes

    _model_registry = _create_provider_classes()

    @staticmethod
    def get_provider(provider_name: str) -> BaseProvider:
        return ProviderFactory._model_registry[provider_name]()

    @staticmethod
    def get_all_providers() -> list[BaseProvider]:
        for provider in ProviderFactory._model_registry.keys():
            yield ProviderFactory.get_provider(provider)
