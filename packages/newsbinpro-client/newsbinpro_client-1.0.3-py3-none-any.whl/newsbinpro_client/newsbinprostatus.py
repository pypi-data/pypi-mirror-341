from typing import List


class NewsbinProStatus:
    """
    Represents the status of the NewsbinPro application, including information about download speed, free space in specific folders, queued file size, and speed samples.
    """

    def __init__(self):
        """
        Manages the initialization of attributes related to download and data folder space,
        file size, and speed metrics for a given object.

        Attributes:
        - speed (int): The current download or processing speed.
        - download_folder_free_space (int): Available free space in the download folder in bytes.
        - data_folder_free_space (int): Available free space in the data folder in bytes.
        - queued_file_size (int): Size of the queued file in bytes.
        - speed_samples (list): A collection of recorded speed samples.
        """
        self._speed = 0
        self._download_folder_free_space = 0
        self._data_folder_free_space = 0
        self._queued_file_size = 0
        self._speed_samples = []

    @property
    def speed(self) -> int:
        """
        :return: The current speed of the object.
        """
        return self._speed

    @property
    def download_folder_free_space(self) -> float:
        """
        :return: The amount of free space available in the download folder.
        """
        return self._download_folder_free_space

    @property
    def download_folder_free_space_str(self) -> str:
        """
        :return: The available free space in the download folder as a human-readable string.
        """
        return self.convert_bytes_to_string(self._download_folder_free_space)

    @property
    def data_folder_free_space(self) -> float:
        """
        :return: The available free space in the data folder.
        """
        return self._data_folder_free_space

    @property
    def data_folder_free_space_str(self) -> str:
        """
        :return: A human-readable string representing the available free space in the data folder. The value is converted from bytes to an appropriate unit (e.g., KB, MB, GB) for easier interpretation.
        """
        return self.convert_bytes_to_string(self._data_folder_free_space)

    @property
    def queued_file_size(self) -> float:
        """
        :return: The size of the file currently queued, represented by the private attribute _queued_file_size.
        """
        return self._queued_file_size

    @property
    def speed_samples(self) -> List[int]:
        """
        :return: Returns the recorded speed samples.
        """
        return self._speed_samples

    def add(self, data: str) -> None:
        """
        :param data: A tab-delimited string containing key-value pairs or data sequences. The keys indicate the type of data (e.g., "Speed", "DownloadFolder", "DataFolder", etc.), and the corresponding values provide the associated numerical data or list of numbers.
        :return: None. This method updates the object's attributes or appends data to the `speed_samples` list based on the input.
        """
        strings = data.split('\t')
        if strings[0] == "Speed":
            self._speed = int(strings[1])
        elif strings[0] == "DownloadFolder":
            self._download_folder_free_space = int(strings[1])
        elif strings[0] == "DataFolder":
            self._data_folder_free_space = int(strings[1])
        elif strings[0] == "Queued":
            self._queued_file_size = int(strings[1])
        elif strings[0] == "Speed Samples":
            for i in range(1, len(strings)):
                self._speed_samples.append(int(strings[i]) * 1000)

    @staticmethod
    def convert_bytes_to_string(size_in_bytes: int) -> str:
        """
        :param size_in_bytes: The size in bytes that needs to be converted into a human-readable string representation.
        :return: A string representing the size in a readable format with appropriate units (e.g., KB, MB, GB).
        """
        units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
        size = float(size_in_bytes)
        unit_index = 0

        # Divide by 1024 until the size is less than 1024 or we reach the largest unit
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.2f} {units[unit_index]}"
