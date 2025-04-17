from typing import Type, Any, TypeVar, cast
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .base_component import BaseComponent
from .json_locators import GeneralLocatorStore, JsonComponent
from selocity import resilient_cached_webelements

T = TypeVar("T", bound="Table")


class Table(BaseComponent):
    general_locator = GeneralLocatorStore.get(JsonComponent.TABLE)

    @property
    @resilient_cached_webelements
    def row_elements(self) -> list[WebElement]:
        return self.root_element.find_elements(By.XPATH, ".//tr")

    @property
    @resilient_cached_webelements
    def header_elements(self) -> list[WebElement]:
        return self.root_element.find_elements(By.XPATH, ".//th")

    class Row:
        def __init__(self, row_element: WebElement, driver: WebDriver):
            self.row_element = row_element
            self.driver = driver

    class Cell:
        def __init__(self, element: WebElement):
            self.element = element

        @property
        def text(self) -> str:
            return self.element.text.strip()

        def __repr__(self) -> str:
            return f"<Cell text='{self.text}'>"

    def get_all_rows(self, driver: WebDriver) -> list[Row]:
        return [self.Row(row, driver) for row in self.row_elements]

    def get_column_headings(self) -> list[str]:
        """
        Returns the text content of all <th> header elements.
        """
        return [header.text.strip() for header in self.header_elements]

    def get_column(self, heading_text: str) -> list[Cell]:
        """
        Given a header label, returns a list of Cell instances corresponding to that column.
        """
        col_index = None
        # Find the index (1-based) of the header with the specified text.
        for i, header in enumerate(self.header_elements):
            if header.text.strip() == heading_text:
                col_index = i + 1
                break
        if col_index is None:
            raise NoSuchElementException(f"No column heading matching '{heading_text}'")

        cells = []
        for row in self.row_elements:
            try:
                # Use a relative XPath to find the <td> in that column.
                cell_element = row.find_element(By.XPATH, f"./td[{col_index}]")
                cells.append(Table.Cell(cell_element))
            except NoSuchElementException:
                # Skip rows that don't have this cell (e.g. header rows)
                continue
        return cells

    @classmethod
    def with_row_components(cls: Type[T], *components: Any) -> Type[T]:
        """
        Dynamically creates a subclass of Table with a Row class that includes the specified components.

        Each item in *components should be either:

          - A component class (subclass of BaseComponent), meaning the first instance found
            inside the row will be attached.
          - A tuple (ComponentClass, ref) where:
                - If ref is a string, ComponentClass.find_in(...) is used with label=ref.
                - If ref is an integer, ComponentClass.find_in(...) is used with index=ref.

        The found component instance is assigned as an attribute on the Row using the lowercase
        component class name.
        """
        class CustomRow(cls.Row):
            def __init__(self, row_element: WebElement, driver: WebDriver):
                super().__init__(row_element, driver)
                for comp in components:
                    if isinstance(comp, tuple):
                        comp: tuple[type[BaseComponent], str]
                        comp_cls, ref = comp
                        if isinstance(ref, str):
                            # Look up by label within the row context.
                            instance = comp_cls.find_in(driver, label=ref, relative_webelement=row_element)
                        elif isinstance(ref, int):
                            # Look up by index within the row context.
                            instance = comp_cls.find_in(driver, relative_webelement=row_element, index=ref)
                        else:
                            raise ValueError(f"Tuple second element must be str (for label) or int (for index), got {type(ref)}")
                    else:
                        comp: type[BaseComponent]
                        comp_cls = comp
                        # Look up the first instance in the row.
                        instance = comp_cls.find_in(driver, relative_webelement=row_element)
                    # Name the attribute based on the component class name in lowercase.
                    attr_name = comp_cls.__name__.lower()
                    setattr(self, attr_name, instance)

        new_table_cls = type("CustomTable", (cls,), {"Row": CustomRow})
        return cast(Type[T], new_table_cls)
