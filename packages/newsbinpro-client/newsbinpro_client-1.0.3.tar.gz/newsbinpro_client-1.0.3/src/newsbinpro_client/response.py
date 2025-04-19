from .statuscode import StatusCode


class Response:
    """
    Represents a response from a certain process or system.

    The `Response` class is used to encapsulate the status code and the message obtained from a given input string. It parses the string to extract a 3-digit status code and the corresponding message.

    Methods:
        - `__init__`: Constructor that parses the input string, extracting and setting the status code and message.
        - `status_code`: Property to get or set the numeric status code.
        - `message`: Property to get or set the response message.
        - `__str__`: String representation combining the status code and message.

    Attributes:
        - `status_code`: An instance of `StatusCode` representing the parsed or default status code.
        - `message`: A string representing the parsed or default response message.
    """

    def __init__(self, response: str):
        """
        Initializes the object with a response string, attempting to parse a status code and message from it.

        :param response: The response string to be parsed. The first three characters are expected to represent a status code (if present), followed by a message starting from the fourth character. If the response string is less than or equal to three characters, the entire response will be treated as the message.
        """
        self._status_code = StatusCode.ParseError
        self.message = ""
        if len(response) > 3:
            try:
                status = int(response[:3])
                self._status_code = StatusCode(status)
            except ValueError:
                pass
            self.message = response[4:]
        else:
            self.message = response

    @property
    def status_code(self) -> StatusCode:
        """
        :return: The HTTP status code associated with the response.
        """
        return self._status_code

    @property
    def message(self) -> str:
        """
        :return: The private attribute `_message`, typically representing the stored message or information associated with the instance.
        """
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        """
        :param value: The new value to be set for the message.
        :return: None
        """
        self._message = value

    def __str__(self) -> str:
        """
        Converts the object into its string representation by formatting the status code
        and message properties of the object.

        :return: A formatted string combining the object's status code and message.
        """
        return f"{self.status_code} {self.message}"
