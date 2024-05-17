import inspect
import sys
from dotenv import load_dotenv
import os
from providers.abstract_providers import BaseProvider
from providers.concrete_providers import *
load_dotenv()

class ProviderFactory:
    @staticmethod
    def _create_provider_classes() -> dict[str, type[BaseProvider]]:
        providers_classes = {}
        provider_subset = os.environ.get("PROVIDER_SUBSET", None)
        if provider_subset:
            provider_subset = provider_subset.split(",")
        for _, obj in inspect.getmembers(sys.modules["providers.concrete_providers"]):
            if inspect.isclass(obj) and issubclass(obj, BaseProvider):
                if provider_subset and obj.NAME in provider_subset:
                    providers_classes[obj.NAME] = obj

        return providers_classes

    _model_registry = _create_provider_classes()

    @staticmethod
    def get_provider(provider_name: str) -> BaseProvider:
        return ProviderFactory._model_registry[provider_name]()

    @staticmethod
    def get_all_provider_names() -> list[BaseProvider]:
        return ProviderFactory._model_registry.keys()
