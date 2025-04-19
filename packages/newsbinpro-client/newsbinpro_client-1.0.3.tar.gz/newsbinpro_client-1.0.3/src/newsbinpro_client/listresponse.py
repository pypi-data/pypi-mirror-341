from .response import Response


class ListResponse(Response):
    """
    Class to represent a response containing a list of items, inheriting from the `Response` base class.

    Methods:
        __init__(response: str): Initializes the `ListResponse` instance with the provided response and initializes the internal list.
        add_list_item(item: str) -> None: Adds a string item to the internal list.
        list_items -> list: Property to retrieve the current list of items.
    """

    def __init__(self, response: str):
        """
        :param response: The response string passed to the constructor, which initializes the base Response class and sets up an empty list for storing list items.
        """
        Response.__init__(self, response)
        self._list_items = []

    def add_list_item(self, item: str) -> None:
        """
        :param item: The string to be added to the list.
        :return: None
        """
        self._list_items.append(item)

    @property
    def list_items(self) -> list:
        """
        :return: The list of items stored in the '_list_items' attribute.
        :rtype: list
        """
        return self._list_items
