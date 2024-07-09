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
                providers_classes[obj.get_provider_name()] = obj
        return providers_classes

    _model_registry = _create_provider_classes()

    @staticmethod
    def get_provider(provider_name: str) -> BaseProvider:
        return ProviderFactory._model_registry[provider_name]()

    @staticmethod
    def get_all_provider_names() -> list[BaseProvider]:
        return ProviderFactory._model_registry.keys()
