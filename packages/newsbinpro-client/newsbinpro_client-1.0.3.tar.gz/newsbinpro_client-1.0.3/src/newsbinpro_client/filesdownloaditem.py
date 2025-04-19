class FilesDownloadItem:
    """
    Represents an item to be downloaded with associated file name and file size.

    Attributes:
        _file_name (str): The name of the file.
        _file_size (int): The size of the file in bytes.
    """

    def __init__(self, value: str):
        """
        :param value: A string expected to contain information in a specific format, where the file name is enclosed in double quotes and followed by the file size as an integer.
        """
        strings = value.split('"')
        self._file_name = strings[1]
        self._file_size = int(strings[2])

    @property
    def file_name(self) -> str:
        """
        :return: The name of the file as a string.
        """
        return self._file_name

    @property
    def file_size(self) -> int:
        """
        :return: The size of the file in bytes.
        """
        return self._file_size
