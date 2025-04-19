class DownloadPartStatus:
    """
    Represents the status of parts of a file being downloaded. Tracks counts related to
    files, parsing status, download status, retries, and pause states.
    """

    def __init__(self, data: str = None):
        """
        Initializes an instance of the class with default values for tracking various counts related to file and download states. Optionally parses input data to populate attributes.

        :param data: Optional string containing data to parse and initialize the attributes accordingly.
        """
        self.fileCount = 0
        self.parCount = 0
        self.downloaded = 0
        self.downloading = 0
        self.incomplete = 0
        self.paused = 0
        self.retries = 0

        if data:
            self.parse_data(data)

    def parse_data(self, data: str) -> None:
        """
        Parses a string containing information about file counts and specific status counts (e.g., downloaded, downloading, incomplete, paused, retries). Updates the corresponding attributes of the object if the input string meets the expected format.

        :param data: A string input containing formatted information about file counts, parsing counts, and associated statuses.
        :return: None. Modifies instance attributes based on the parsed data.
        """
        right_brace_index = data.find(']')
        if right_brace_index == -1:
            return
        temp = data[0:right_brace_index]
        parts = temp.split(' ')
        if len(parts) != 4:
            return

        self.fileCount = int(parts[0][1:])
        self.parCount = int(parts[2])

        temp = data[right_brace_index + 1:]
        parts = temp.split(' ')
        for part in parts:
            sub_parts = part.split(':')
            key = sub_parts[0]
            value = int(sub_parts[1])
            if key == 'D':
                self.downloaded = value
            elif key == 'DL':
                self.downloading = value
            elif key == 'In':
                self.incomplete = value
            elif key == 'P':
                self.paused = value
            elif key == 'R':
                self.retries = value

    def __str__(self):
        """
        Returns a string representation of the current instance, summarizing the state of various attributes.

        :return: A formatted string containing the values of `fileCount`, `parCount`, `downloaded`, `downloading`, `incomplete`, `paused`, and `retries`.
        """
        return f'fileCount:{self.fileCount};parCount:{self.parCount};downloaded:{self.downloaded};downloading:{self.downloading};' \
               f'incomplete:{self.incomplete};paused:{self.paused};retries:{self.retries}'
