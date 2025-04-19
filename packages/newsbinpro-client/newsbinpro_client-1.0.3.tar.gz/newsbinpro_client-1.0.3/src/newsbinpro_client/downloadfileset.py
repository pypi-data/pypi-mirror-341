import datetime
from enum import Enum
from typing import List

from .downloadpartstatus import DownloadPartStatus


class FileSetType(Enum):
    """
    An enumeration that defines the types of file sets used in the application.

    Attributes:
        Header: Represents a file set containing header files. Assigned the value 1.
        Download: Represents a file set used for downloading files. Assigned the value 2.
        Repair: Represents a file set used for file repair operations. Assigned the value 3.
        Unpack: Represents a file set used for unpacking files. Assigned the value 4.
    """
    Header = 1
    Download = 2
    Repair = 3
    Unpack = 4


class DownloadFileSet:
    """
        Represents a set of downloadable files, providing functionality to parse and manage file-related properties
        and statuses based on the input data.
    """

    def __init__(self, data):
        """
        Initializes the instance by parsing the provided tab-delimited data to set internal attributes.

        :param data: A tab-delimited string containing attributes for initializing the instance. Expected fields
                     include ID, subject, status, pause status, and others necessary for file type determination.
        """
        self._file_size = None
        self._time_stamp = None
        self._download_path = None
        self._downloaded_size = None
        self._downloaded_current_size = None
        self._status = None
        self._poster = None
        self._partStatus = DownloadPartStatus()

        strings = data.split('\t')
        self._item_id = int(strings[0])
        self._subject = strings[1]
        self._status = strings[8]
        self._file_set_type = self._get_file_set_type(self.subject, self._status)
        self._isPaused = strings[9] == '1'
        decisions = {
            FileSetType.Header: self.parse_header,
            FileSetType.Download: self.parse_download,
            FileSetType.Repair: self.parse_repair,
            FileSetType.Unpack: self.parse_unpack,
        }
        parse_method = decisions.get(self._file_set_type, lambda: None)
        parse_method(strings)

    @property
    def item_id(self) -> int:
        """
        :return: The unique identifier of the object.
        :rtype: int
        """
        return self._item_id

    @property
    def subject(self) -> str:
        """
        :return: The subject as a string.
        """
        return self._subject

    @property
    def file_size(self) -> int:
        """
        :return: The size of the file in bytes.
        """
        return self._file_size

    @property
    def time_stamp(self) -> datetime.datetime:
        """
        :return: The timestamp as a datetime object.
        :rtype: datetime.datetime
        """
        return self._time_stamp

    @property
    def poster(self) -> str:
        """
        :return: The poster string that represents the corresponding attribute.
        """
        return self._poster

    def parse_header(self, strings: List[str]) -> None:
        """
        Parses the header information from a list of strings, extracting and processing specific values to update properties.

        :param strings: List of strings containing header-related information. It is expected to have specific indices populated with data for subject and size calculations.
        :return: None
        """
        self._subject = 'Header download' if strings[4] == '' else strings[4]
        substrings = strings[7].split('/')
        self._downloaded_current_size = self._get_size(substrings[0])
        self._downloaded_size = self._get_size(substrings[1])

    def parse_download(self, strings: List[str]) -> None:
        """
        Parses and extracts information related to a download from a list of strings.

        :param strings: A list of strings containing specific information about the download.
        :return: None
        """
        self._file_size = int(strings[2])
        self._time_stamp = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(strings[3]))
        self._poster = strings[4]
        self._download_path = strings[5]
        substrings = strings[7].split('/')
        self._downloaded_current_size = self._get_size(substrings[0])
        self._downloaded_size = self._get_size(substrings[1])
        self._partStatus = DownloadPartStatus(self._status)

    def parse_repair(self, strings: List[str]) -> None:
        """
        Parses and extracts information related to a repair from a list of strings.

        :param strings: List of strings passed as input. Not directly used in the function.
        :return: None. This method processes and updates internal instance variables.
        """
        substrings = self._status.split('%')
        self._downloaded_current_size = int(substrings[0][12:])
        self._downloaded_size = 100

    def parse_unpack(self, strings: List[str]) -> None:
        """
        Parses the input list of strings and updates the object's download status.

        :param strings: A list of strings to be parsed for updating download status.
        :return: None
        """
        substrings = self._status.split('%')
        self._downloaded_current_size = int(substrings[0][12:])
        self._downloaded_size = 100

    @staticmethod
    def _get_file_set_type(subject: str, status: str) -> FileSetType:
        """
        Get FileSetType from subject and status.

        :param subject: A string representing the subject or type of the file set.
        :param status: A string representing the current status or processing state of the file set.
        :return: A FileSetType enumerator indicating the type of the file set based on the subject and status provided.
        """
        if subject == '':
            return FileSetType.Header
        elif status.startswith('PAR'):
            return FileSetType.Repair
        elif status.startswith('UnRAR'):
            return FileSetType.Unpack
        else:
            return FileSetType.Download

    @staticmethod
    def _get_size(size_string: str) -> int:
        """
        Get size string

        :param size_string: A string representing a size with a value and unit (e.g., '10 KB', '5 MB', '2 GB').
        :return: The size in bytes as an integer.
        """
        strings = size_string.split(' ')
        result = int(strings[0])
        if strings[1] == 'KB':
            result *= 1024
        elif strings[1] == 'MB':
            result *= 1024 * 1024
        elif strings[1] == 'GB':
            result *= 1024 * 1024 * 1024
        return result
