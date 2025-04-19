import datetime


class GroupFileSet:
    """
    Represents a group file set with associated metadata such as ID, subject, file size, timestamp, poster,
    file count, parity count, and an indicator of whether it is old.

    Attributes:
        item_id (int): Unique identifier for the group file set.
        subject (str): Subject or title of the group file set.
        file_size (int): Size of the file in the group file set, in bytes.
        time_stamp (datetime.datetime): Timestamp representing the creation or upload time of the file set.
        poster (str): Name or identifier of the person or entity that posted the file set.
        file_count (int): Number of files included in the file set.
        par_count (int): Number of parity files in the file set.
        is_old (bool): Flag indicating whether the file set is considered old.

    Methods:
        __init__(data):
            Parses a tab-separated string to initialize all the attributes of the group file set.
            Converts and formats certain attributes to appropriate data types.

        __str__():
            Returns a formatted string representation of the group file set showing all its attributes.
    """

    def __init__(self, data: str):
        """
        Initializes an object with the given tab-separated input data and parses its properties.

        :param data: A tab-separated string containing values in the following order:
                     item_id (int), subject (str), file size (int), timestamp (int in seconds),
                     poster (str), file count (int), par count (int), and is_old (str, '0' or '1').
        """
        strings = data.split('\t')

        self._item_id = int(strings[0])
        self._subject = strings[1]
        self._file_size = int(strings[2])
        # Initialize as Unix epoch (1970-Jan-1 00:00:00)
        self._time_stamp = datetime.datetime(1970, 1, 1, 0, 0, 0)
        # Add timestamp in seconds parsed from the string data
        self._time_stamp += datetime.timedelta(seconds=int(strings[3]))
        self._poster = strings[4]
        self._file_count = int(strings[5])
        self._par_count = int(strings[6])
        self._is_old = strings[7] == '0'

    @property
    def item_id(self) -> int:
        """
        :return: The unique identifier associated with the object.
        """
        return self._item_id

    @property
    def subject(self) -> str:
        """
        :return: The value of the subject property.
        """
        return self._subject

    @property
    def file_size(self) -> int:
        """
        :return: The size of the file as an integer.
        """
        return self._file_size

    @property
    def time_stamp(self) -> datetime.datetime:
        """
        :return: The current timestamp value.
        """
        return self._time_stamp

    @property
    def poster(self) -> str:
        """
        :return: The poster associated with the object, which is typically used to access or reference specific content or resources.
        """
        return self._poster

    @property
    def file_count(self) -> int:
        """
        :return: The current count of files as an integer
        """
        return self._file_count

    @property
    def par_count(self) -> int:
        """
        :return: The current value of the `_par_count` attribute.
        :rtype: int
        """
        return self._par_count

    @property
    def is_old(self) -> bool:
        """
        :return: Returns a boolean value indicating whether the item is considered old.
        """
        return self._is_old

    def __str__(self) -> str:
        """
        :return: A string representation of the object containing its properties: item_id, subject, file_size, time_stamp, poster, file_count, par_count, and is_old, formatted as key=value pairs separated by semicolons.
        """
        return f"item_id={self.item_id};subject={self.subject};fileSize={self.file_size};timeStamp={self.time_stamp};poster={self.poster};fileCount={self.file_count};parCount={self.par_count};isOld={self.is_old}"
