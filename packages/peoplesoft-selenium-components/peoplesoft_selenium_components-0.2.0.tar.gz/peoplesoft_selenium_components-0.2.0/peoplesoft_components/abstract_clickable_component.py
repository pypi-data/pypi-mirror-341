from functools import cached_property

from .abstract_input_component import AbstractInputComponent


class AbstractClickableComponent(AbstractInputComponent):
    @cached_property
    def _is_submitting(self):
        if self._is_always_submitting:
            return True
        on_change_value = self.root_element.get_attribute("onchange")
        href_value = self.root_element.get_attribute("href")
        values = [on_change_value, href_value]
        return any("submitaction" in (val or "").lower() for val in values)

    def click(self):
        self.root_element.click()
        if self._is_submitting:
            self._wait_for_spinner()

    def click_with_save_spinner(self):
        self.click()
        self._wait_for_saved_spinner()
