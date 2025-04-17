from . import BaseComponent
from .json_locators import GeneralLocatorStore, JsonComponent


class TextInput(BaseComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.TEXT)
