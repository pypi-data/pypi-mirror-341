from datetime import datetime, timedelta


class FilesFileSet:
    """
    Represents a file with metadata extracted from a tab-separated string.

    Attributes:
        item_id (int): Identifier of the file.
        subject (str): Subject or description of the file.
        file_size (int): Size of the file in bytes.
        time_stamp (datetime): Timestamp of the file creation or modification based on seconds since the epoch.
        poster (str): Name or identifier of the person who posted the file.
        file_name (str): Name of the file.

    Methods:
        __init__(data):
            Initializes the FilesFileSet object by parsing a tab-separated string to populate attributes.

        __str__():
            Returns a string representation of the FilesFileSet highlighting its attribute values.
    """

    def __init__(self, data: str):
        strings = data.split('\t')
        self._item_id = int(strings[0])
        self._subject = strings[1]
        self._file_size = int(strings[2])
        self._time_stamp = datetime(1970, 1, 1, 0, 0, 0) + timedelta(seconds=int(strings[3]))
        self._poster = strings[4]
        self._file_name = strings[5]

    @property
    def item_id(self) -> int:
        return self._item_id

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def file_size(self) -> int:
        return self._file_size

    @property
    def time_stamp(self) -> datetime:
        return self._time_stamp

    @property
    def poster(self) -> str:
        return self._poster

    @property
    def file_name(self) -> str:
        return self._file_name

    def __str__(self) -> str:
        return f"item_id={self.item_id};subject={self.subject};file_size={self.file_size};time_stamp={self.time_stamp};poster={self.poster};file_name={self.file_name}"
