from datetime import datetime, timedelta


class WishFileSet():
    """
    Represents a file set with metadata such as ID, subject, file size, timestamp, poster, download path, status string, file count, and par count, parsed from a tab-delimited input string.

    Attributes:
        item_id (int): Identifier of the file set.
        subject (str): The subject or title of the file set.
        file_size (int): The size of the file set in bytes.
        time_stamp (datetime): The timestamp associated with the file set, calculated from the epoch time in seconds.
        poster (str): The name or identifier of the file set's poster.
        download_path (str): The path where the file is downloaded.
        status_string (str): The unparsed status string associated with the file set.
        file_count (int): The number of files in the file set, extracted from the status string.
        par_count (int): The number of parity files (PAR files) in the file set, extracted from the status string.

    Methods:
        __init__: Initializes the WishFileSet instance by parsing and storing details from a tab-delimited string.
        __str__: Returns a string representation of the file set with its key attributes.
    """

    def __init__(self, data: str):
        """
        Initializes a new instance of the class by parsing and processing the input data string.

        :param data: Input string containing delimited fields with tab ('\t') separators. The fields are expected in the following order:
                     - ID (integer)
                     - Subject (string)
                     - File size (integer)
                     - Timestamp (number of seconds since UNIX epoch)
                     - Poster (string)
                     - Download path (string)
                     - Status string (enclosed in square brackets with specific format)
        """
        strings = data.split('\t')
        self._item__id = int(strings[0])
        self._subject = strings[1]
        self._file_size = int(strings[2])
        self._time_stamp = datetime(1970, 1, 1) + timedelta(seconds=int(strings[3]))
        self._poster = strings[4]
        self._download_path = strings[5]
        self._status_string = strings[8]
        sub_strings = self._status_string.strip('[').split(']')[0].split(' ')
        self._file_count = int(sub_strings[0])
        self._par_count = int(sub_strings[2])

    @property
    def item_id(self) -> int:
        """
        :return: The identifier of the object.
        """
        return self._item__id

    @property
    def subject(self) -> str:
        """
        :return: The subject associated with the instance.
        """
        return self._subject

    @property
    def file_size(self) -> float:
        """
        :return: The size of the file.
        """
        return self._file_size

    @property
    def time_stamp(self) -> datetime:
        """
        :return: The current timestamp associated with the object. This represents the time when the object was created or last updated, depending on its implementation.
        """
        return self._time_stamp

    @property
    def poster(self) -> str:
        """
        :return: The poster property, which retrieves the value of the private attribute '_poster'.
        """
        return self._poster

    @property
    def download_path(self) -> str:
        """
        :return: The current download path.
        """
        return self._download_path

    @property
    def status_string(self) -> str:
        """
        :return: The status string representing the current state.
        :rtype: str
        """
        return self._status_string

    @property
    def file_count(self) -> int:
        """
        :return: The current count of files.
        """
        return self._file_count

    @property
    def par_count(self) -> int:
        """
        :return: The value of the private attribute `_par_count`
        """
        return self._par_count

    def __str__(self) -> str:
        """
        Converts the object to its string representation.

        :return: A string containing the concatenated attributes of the object in the format:
                 item_id=<item_id>;subject=<subject>;file_size=<file_size>;time_stamp=<time_stamp>;
                 poster=<poster>;download_path=<download_path>;file_count=<file_count>;
                 par_count=<par_count>.
        """
        return f"item_id={self.item_id};subject={self.subject};file_size={self.file_size};time_stamp={self.time_stamp};poster={self.poster};download_path={self.download_path};file_count={self.file_count};par_count={self.par_count}"
