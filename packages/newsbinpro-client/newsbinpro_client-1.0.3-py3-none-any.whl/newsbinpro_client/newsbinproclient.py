import asyncio
import hashlib
import inspect
import logging
import os
from asyncio import StreamReader, StreamWriter
from typing import Callable, List, BinaryIO

from .command import Command
from .downloadfileset import DownloadFileSet
from .filesdownloaditem import FilesDownloadItem
from .filesfileset import FilesFileSet
from .groupfileset import GroupFileSet
from .groupofgroupstree import GroupOfGroupsTree
from .listresponse import ListResponse
from .newsbinprostatus import NewsbinProStatus
from .response import Response
from .statuscode import StatusCode
from .wishfileset import WishFileSet

"""
Newsbin Pro client library
https://github.com/jonnybergdahl/Python-NewsbinPro-Client

Author: Jonny Bergdahl
Date: 2025-01-02
"""


class NewsbinProClient:
    """
    A client for connecting to a NewsbinPro server for remote control.
    """

    def __init__(self,
                 server_address: str,
                 port: int,
                 password: str,
                 on_connected_callback: Callable[[], None] = None,
                 on_disconnected_callback: Callable[[], None] = None,
                 on_data_sent: Callable[[str], None] = None,
                 on_data_received: Callable[[str], None] = None,
                 on_received_list_item: Callable[[str], None] = None,
                 log_level: int = logging.INFO):
        """
        Initializes the NewsbinProClient object.

        :param server_address: The address of the Newsbin Pro server.
        :type server_address: str
        :param port: The port to connect to the server.
        :type port: int
        :param password: The password for server authentication.
        :type password: str
        :param on_connected_callback: Optional; callback executed after a successful connection.
        :type on_connected_callback: Callable[[], None] or None
        :param on_disconnected_callback: Optional; callback executed after disconnection.
        :type on_disconnected_callback: Callable[[], None] or None
        :param on_data_sent: Optional; callback executed after data is sent to the server.
        :type on_data_sent: Callable[[str], None] or None
        :param on_data_received: Optional; callback executed after receiving data from the server.
        :type on_data_received: Callable[[str], None] or None
        :param on_received_list_item: Optional; callback for when a new list item is received.
        :type on_received_list_item: Callable[[str], None] or None
        :param log_level: The logging level for this client instance. Default is `logging.INFO`.
        :type log_level: int
        """
        self.server_address = server_address
        self.port = port
        self.password = password
        self.newsbin_version = None

        self._reader: StreamReader = None
        self._writer: StreamWriter = None

        self._on_connected: Callable[[], None] = on_connected_callback
        self._on_disconnected: Callable[[], None] = on_disconnected_callback
        self._on_data_sent: Callable[[str], None] = on_data_sent
        self._on_data_received: Callable[[str], None] = on_data_received
        self._on_received_list_item: Callable[[str], None] = on_received_list_item

        logging.basicConfig(
            level=log_level,  # Set the log level
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    @property
    def connected(self):
        """
        :return: Returns True if the client is connected, otherwise, returns False.
        """
        return self._writer is not None and not self._writer.is_closing()

    async def connect(self, timeout: int = 30):
        """
        Establishes a connection to the NewsbinPro server.

        If authentication is required, it attempts to authenticate
        using the provided password.

        :param timeout: The maximum time (in seconds) to wait for the connection. Default is 30 seconds.
        :type timeout: int
        :raises Exception: If authentication with the server fails.
        """
        self._reader, self._writer = await asyncio.wait_for(
            asyncio.open_connection(self.server_address, self.port),
            timeout=timeout
        )
        response = await self.get_response()
        if response.status_code == StatusCode.AuthNeedAuth:
            parts = response.message.split('-')
            if len(parts) == 2:
                self.newsbin_version = parts[0].strip()
                password_salt = parts[1][1:17]
                auth_string = self.get_auth_string(self.password, password_salt)
                response = await self.send_command(Command.Auth, auth_string)

        if not response.status_code == StatusCode.OK:
            self._dispose_connection()
            raise Exception("Authentication failed")

        if self._on_connected:
            if inspect.iscoroutinefunction(self._on_connected):
                await asyncio.create_task(self._on_connected())
            else:
                self._on_connected()

    async def disconnect(self):
        """
        Disconnects the client by sending the quit command to the server.
        Handles the client disconnection event and disposes of the connection.

        :return: None
        """
        await self.send_command(Command.Quit)
        if self._on_disconnected:
            if inspect.iscoroutinefunction(self._on_disconnected):
                await asyncio.create_task(self._on_disconnected())
            else:
                self._on_disconnected()
        self._dispose_connection()

    def _dispose_connection(self):
        """
        Closes and disposes of the reader and writer connections.

        :return: None
        """
        if self._writer:
            self._writer.close()
            self._writer = None
        if self._reader:
            self._reader = None

    # Status methods

    async def update(self) -> bool:
        """
        Sends an update command.

        :return: True if the update command was successful (status is OK), otherwise False.
        """
        result = await self.send_command(Command.Update)
        return result.status_code == StatusCode.OK

    async def save(self) -> bool:
        """
        Saves the current configuration file.

        :return: A boolean indicating whether the save operation was successful.
        """
        result = await self.send_command(Command.Save)
        return result.status_code == StatusCode.OK

    async def close(self) -> bool:
        """
        Closes the Newsbin Pro application. No further communication is possible after this call.

        :return: True if the command execution was successful and the status code is OK, False otherwise
        """
        result = await self.send_command(Command.Close)
        return result.status_code == StatusCode.OK

    async def get_status(self) -> NewsbinProStatus:
        """
        Retrieves the status of NewsbinPro by sending a status command
        and aggregating the response into a NewsbinProStatus object.

        :return: An instance of NewsbinProStatus containing the aggregated status data.
        """
        result = NewsbinProStatus()
        response = await self.send_list_command(Command.Status)
        for data in response.list_items:
            result.add(data)
        return result

    # TODO:
    # set_var(self, section, name, value):
    # get_var(self, section, name) -> str:
    # get_section(self, section) -> List[something]:

    async def get_bandwidth_limiter_state(self):
        """
        Sends a command to check the state of the bandwidth limiter and returns its status.

        :return: True if the bandwidth limiter is on, False otherwise.
        """
        response = await self.send_command(Command.Bwl)
        return response.status_code == StatusCode.StatusBwLimiterOn

    async def set_bandwidth_limiter_state(self, state: bool):
        """
        :param state: A boolean value indicating the desired state of the bandwidth limiter. True to turn it on, False to turn it off.
        :return: A boolean indicating whether the operation to set the bandwidth limiter state was successful.
        """
        response = await self.send_command(Command.Bwl, "ON" if state else "OFF")
        return response.status_code == StatusCode.StatusBwLimiterOn

    async def get_paused_state(self):
        """
        Sends a pause command to check whether the system is in a paused state.

        :return: A boolean indicating if the system is in a paused state. True if the system is paused, False otherwise.
        """
        response = await self.send_command(Command.Pause)
        return response.status_code == StatusCode.StatusPauseOn

    async def set_paused_state(self, state: bool):
        """
        :param state: A boolean value indicating the desired paused state. True to set the state to paused, False to set it to unpaused.
        :return: A boolean indicating whether the operation was successful. Returns True if the pause state was successfully set to the desired value, otherwise False.
        """
        response = await self.send_command(Command.Pause, "ON" if state else "OFF")
        return response.status_code == StatusCode.StatusPauseOn

    # Group List

    async def list_groups(self) -> ListResponse:
        """
        Lists all subscribed groups.

        :return: A ListResponse object containing the details of all groups.
        """
        response = await self.send_list_command(Command.ListGroups)
        return response

    async def list_gogs(self) -> ListResponse:
        """
        Lists all group topics (parents)

        :return: The response containing the list of Gogs.
        :rtype: ListResponse
        """
        response = await self.send_list_command(Command.ListGogs)
        return response

    async def list_children(self, gog_name: str) -> ListResponse:
        """
        Lists all children of a particular parent topic.

        :param gog_name: The name of the group or object whose children need to be listed.
        :return: A ListResponse containing the children of the specified group or object.
        """
        response = await self.send_list_command(Command.ListChildren, gog_name)
        return response

    async def list_children_details(self, gog_name: str) -> ListResponse:
        """
        Lists all children details of a particular parent topic.

        :param gog_name: The name of the group or object whose children details need to be listed.
        :return: A ListResponse containing the details of the children for the specified group or object.
        """
        response = await self.send_list_command(Command.ListChildrenDetails, gog_name)
        return response

    async def list_group_of_groups_with_children(self) -> GroupOfGroupsTree:
        """
        Lists groups and their respective child groups into a tree structure.

        :return: GroupOfGroupsTree object representing the hierarchy of groups and their children.
        """
        response = await self.send_list_command(Command.ListChildren)
        result = GroupOfGroupsTree()
        for group_name in response.list_items:
            sub_response = await self.send_list_command(Command.ListChildrenDetails)
            for child_name in sub_response.list_items:
                result.add(group_name, child_name)

        return result

    # Server methods

    async def list_servers(self) -> ListResponse:
        """
        Sends a command to list all available servers and returns the response.

        :return: An object of type ListResponse containing the list of servers.
        """
        return await self.send_list_command(Command.ListServers)

    # Filter methods

    async def list_filters(self) -> ListResponse:
        """
        Lists all filters

        :return: A ListResponse object containing the available filters.
        """
        return await self.send_list_command(Command.ListFilters)

    async def set_filter_min_size(self, min_size: int) -> bool:
        """
        Sets the minimum size filter for when search or group loading is performed.

        :param min_size: The minimum size value to set for the filter.
        :type min_size: int
        :return: A boolean indicating whether the command to set the filter minimum size was successful.
        :rtype: bool
        """
        response = await self.send_command(Command.FilterSetMinSize, str(min_size))
        return response.status_code == StatusCode.OK

    async def set_filter_max_size(self, max_size: int) -> bool:
        """
        Sets the maximum size filter for when search or group loading is performed.

        :param max_size: The maximum size to set for the filter as an integer.
        :return: A boolean indicating whether the operation to set the maximum size was successful.
        """
        response = await self.send_command(Command.FilterSetMaxSize, str(max_size))
        return response.status_code == StatusCode.OK

    async def add_group_filter(self, group_name: str) -> bool:
        """
        Adds a group or a group of groups if a topic is selected. The topic is expanded into the list of current groups.
        These groups are used by "Load" and "Search" to specify what groups to look into.

        :param group_name: The name of the group filter to add.
        :return: A boolean indicating whether the group filter was successfully added.
        """
        response = await self.send_command(Command.FilterAddGroupFilter, group_name)
        return response.status_code == StatusCode.OK

    async def set_filter_age(self, hours: int) -> bool:
        """
        Sets the maximum age of the sets in the display buffer.

        :param hours: The age limit for the filter in hours.
        :return: A boolean value indicating if the filter age was successfully set.
        """
        response = await self.send_command(Command.FilterSetAge, str(hours))
        return response.status_code == StatusCode.OK

    async def set_text_filter(self, text: str) -> bool:
        """
        Sets the current text filter. Text quoting is optional (but recommended).
        An empty string will clear the text filter.

        :param text: The text to set as the filter.
        :return: A boolean value indicating whether setting the text filter was successful or not.
        """
        response = await self.send_command(Command.FilterSetTextFilter, text)
        return response.status_code == StatusCode.OK

    async def hide_old(self, hide: bool) -> bool:
        """
        Enable/Disable the "hide old" filter

        :param hide: A boolean value indicating whether to hide old filters. If True, old filters will be hidden; otherwise, they will not.
        :return: A boolean value indicating whether the command to hide old filters was successfully executed.
        """
        response = await self.send_command(Command.FilterHideOld, "1" if hide else "0")
        return response.status_code == StatusCode.OK

    async def enable_filters(self, enabled: bool) -> bool:
        """
        Enable/Disable filter.

        :param enabled: Boolean value indicating whether to enable (True) or disable (False) filters.
        :return: Boolean value indicating whether the operation was successful.
        """
        response = await self.send_command(Command.FilterEnableFilters, "1" if enabled else "0")
        return response.status_code == StatusCode.OK

    async def clear_filters(self, clear: bool) -> bool:
        """
        Clears the existing size filters and groups.

        :param clear: A boolean value indicating whether to clear all filters (True) or not (False).
        :return: A boolean value representing whether the command succeeded (True) or failed (False).
        """
        response = await self.send_command(Command.FilterClear, "1" if clear else "0")
        return response.status_code == StatusCode.OK

    async def mark_old(self, item_id: int) -> bool:
        """
        Tag the files as "Old" both in the display list and on disk.

        :param item_id: The unique identifier of the filter to be marked as old.
        :return: True if the filter was successfully marked as old, otherwise False.
        """
        response = await self.send_command(Command.FilterMarkOld, str(item_id))
        return response.status_code == StatusCode.OK

    async def mark_all_old(self) -> bool:
        """
        Sends a command to mark all items as old.

        :return: True if the operation was successful, False otherwise.
        """
        response = await self.send_command(Command.FilterMarkAllOld)
        return response.status_code == StatusCode.OK

    async def set_filter_profile(self, profile_name: str) -> bool:
        """
        Set filter profile.

        :param profile_name: The name of the filter profile to set.
        :return: A boolean indicating whether the operation was successful.
        """
        response = await self.send_command(Command.FilterSetProfile, profile_name)
        return response.status_code == StatusCode.OK

    # Search methods

    async def search_local(self, min_age: int, max_age: int, search_string: str) -> bool:
        """
        Searches the groups listed using "AddGroupFilter" or all groups if no groups have been added.
        It loads each group in turn and only saves the items in memory that match the filter string and size filters.
        These matched items are added to the display buffer and become accessible using the "Loaded" interface.
        The min age/max age set how many day in the past to search from. So, a setting of 100 and 0 means
        "from 100 days ago to 0 days ago( Now)". Only finds records from groups that have actually
        had headers downloaded.

        :param min_age: The minimum age to filter the search results.
        :param max_age: The maximum age to filter the search results.
        :param search_string: The string to search for in the local data.
        :return: A boolean indicating whether the search operation was successful.
        """
        response = await self.send_command(Command.SearchLocal, str(min_age), str(max_age), search_string)
        return response.status_code == StatusCode.OK

    async def search_internet(self, min_age: int, max_age: int, search_string: str) -> bool:
        """
        Searches using the search server, the groups listed using "AddGroupFilter" or all groups if no groups have
        been added. It loads each group in turn and only saves the items in memory that match the filter string
        and size filters. These matched items are added to the display buffer and become accessible using the
        "Loaded" interface. The min age/max age set how many day in the past to search from.
        So, a setting of 100 and 0 means "from 100 days ago to 0 days ago( Now)".

        :param min_age: The minimum age to include in the search criteria.
        :param max_age: The maximum age to include in the search criteria.
        :param search_string: The term or phrase to search for on the internet.
        :return: A boolean indicating whether the search operation was successful.
        """
        response = await self.send_command(Command.SearchInternet, str(min_age), str(max_age), search_string)
        return response.status_code == StatusCode.OK

    # Group methods

    async def load_group(self, min_age: int, max_age: int) -> int:
        """
        Load a group. To load the last 10 days of records for instance the min_age would be 10 and the max_age would
        be zero. It counts backwards. load_group(20, 10) would load posts from 20 days ago to 10 days ago.

        :param min_age: The minimum age for filtering the group.
        :param max_age: The maximum age for filtering the group.
        :return: The result of the command, representing the number of entries loaded.
        """
        return await self.send_long_command(Command.GroupLoad, str(min_age), str(max_age))

    async def clear_group(self) -> bool:
        """
        Clear a group

        :return: Returns True if the group is successfully cleared, False otherwise.
        """
        response = await self.send_command(Command.GroupClear)
        return response.status_code == StatusCode.OK

    async def delete_from_group(self, group_id: int) -> bool:
        """
        Delete from a group.

        :param group_id: The identifier of the group to be deleted.
        :return: A boolean indicating whether the deletion was successful.
        """
        response = await self.send_command(Command.GroupDelete, str(group_id))
        return response.status_code == StatusCode.OK

    # Loaded methods

    async def get_loaded_count(self) -> int:
        """
        Gets the number of loaded items.

        :return: The total count of loaded items.
        """
        return await self.send_long_command(Command.LoadedCount)

    async def list_loaded(self, start_index: int, end_index: int) -> List[GroupFileSet]:
        """
        List the loaded items.

        :param start_index: The starting index from which to begin retrieving the loaded file sets.
        :param end_index: The ending index at which to stop retrieving the loaded file sets.
        :return: A list of GroupFileSet objects representing the loaded file sets within the specified range.
        """
        response = await self.send_list_command(Command.LoadedList, str(start_index), str(end_index))
        result = []
        for file_set in response.list_items:
            result.append(GroupFileSet(file_set))
        return result

    async def sort_loaded(self, column: int, ascending: bool) -> bool:
        """
        Sorts the loaded items according to the specified column.

        :param column: The index of the column to sort.
        :param ascending: A boolean indicating the sort order. If True, sort in ascending order; if False, sort in descending order.
        :return: A boolean indicating whether the sorting operation was successful.
        """
        response = await self.send_command(Command.LoadedSort, str(column), str(ascending))
        return response.status_code == StatusCode.OK

    async def clear_loaded(self) -> bool:
        """
        Clears the loaded list.

        :return: Returns True if the command was successfully executed, False otherwise.
        """
        response = await self.send_command(Command.LoadedClear)
        return response.status_code == StatusCode.OK

    async def find_loaded(self, text: str) -> List[GroupFileSet]:
        """
        Finds matching items in the loaded list.

        :param text: The text used to search and filter the loaded file sets.
        :return: A list of GroupFileSet instances representing the loaded file sets that match the search criteria.
        """
        response = await self.send_list_command(Command.LoadedFind, text)
        result = []
        for file_set in response.list_items:
            result.append(GroupFileSet(file_set))
        return result

    async def download_from_loaded(self, item_id: int) -> bool:
        """
        Download a file from the loaded list.

        :param item_id: The identifier of the item to be downloaded.
        :return: True if the download operation was successful, False otherwise.
        """
        response = await self.send_command(Command.LoadedDownload, str(item_id))
        return response.status_code == StatusCode.OK

    async def get_nzb_from_loaded(self, min_index: int, max_index: int) -> bool:
        """
        :param min_index: The minimum index of the NZB to retrieve.
        :param max_index: The maximum index of the NZB to retrieve.
        :return: True if the NZB was successfully retrieved, False otherwise.
        """
        response = await self.send_command(Command.LoadedGetNzb, str(min_index), str(max_index))
        return response.status_code == StatusCode.OK

    # Downloads methods

    async def get_downloads_count(self) -> int:
        """
        Sends a command to retrieve the total downloads count.

        :return: The number of downloads.
        :rtype: int
        """
        return await self.send_long_command(Command.DownloadsCount)

    async def lock_downloads(self) -> bool:
        """
        Sends a command to lock the downloads and returns whether the operation was successful.

        :return: True if the downloads were successfully locked, False otherwise
        """
        response = await self.send_command(Command.DownloadsLock)
        return response.status_code == StatusCode.OK

    async def unlock_downloads(self) -> bool:
        """
        Sends a command to unlock downloads and checks the response status.

        :return: True if the downloads were successfully unlocked, False otherwise.
        """
        response = await self.send_command(Command.DownloadsUnlock)
        return response.status_code == StatusCode.OK

    async def get_downloads_list(self, start_index: int, end_index: int) -> List[DownloadFileSet]:
        """
        :param start_index: The starting index for the range of downloads to retrieve.
        :param end_index: The ending index for the range of downloads to retrieve.
        :return: A list of DownloadFileSet objects representing the downloads in the specified range.
        """
        response = await self.send_list_command(Command.DownloadsList, str(start_index), str(end_index))
        result = []
        for downloads_set in response.list_items:
            result.append(DownloadFileSet(downloads_set))

        return result

    async def sort_downloads_list(self, column: int, ascending: bool) -> bool:
        """
        :param column: The index of the column by which the downloads list should be sorted.
        :param ascending: A boolean indicating whether the sorting should be in ascending order. If False, sorting will be in descending order.
        :return: A boolean indicating whether the operation was successful (True) or not (False).
        """
        response = await self.send_list_command(Command.DownloadsSort, str(column), str(ascending))
        return response.status_code == StatusCode.OK

    async def clear_downloads(self) -> bool:
        """
        Clears the current list of downloads.

        Sends a command to clear all download entries and checks the response status code to confirm the action was successful.

        :return: True if the list of downloads is successfully cleared, False otherwise.
        """
        response = await self.send_command(Command.DownloadsClear)
        return response.status_code == StatusCode.OK

    async def find_in_downloads(self, text: str) -> bool:
        """
        :param text: The text to search for in the download list.
        :return: A boolean indicating whether the search operation was successful (True if the status code equals OK, False otherwise).
        """
        response = await self.send_list_command(Command.DownloadsFind, text)
        return response.status_code == StatusCode.OK

    async def assemble_download(self, item_id: int) -> bool:
        """
        :param item_id: The identifier of the download to be assembled.
        :return: A boolean value indicating whether the assembly of the download was successful.
        """
        response = await self.send_command(Command.DownloadsAssemble, str(item_id))
        return response.status_code == StatusCode.OK

    async def pause_download(self, item_id: int) -> bool:
        """
        Pauses an active download by its identifier.

        :param item_id: The unique identifier of the download to be paused.
        :return: True if the pause command was successfully executed, False otherwise.
        """
        response = await self.send_command(Command.DownloadsPause, str(item_id))
        return response.status_code == StatusCode.OK

    async def resume_download(self, item_id: int) -> bool:
        """
        Resumes a paused download for the specified download ID.

        :param item_id: The unique identifier of the download to be resumed.
        :return: True if the download was successfully resumed, False otherwise.
        """
        response = await self.send_command(Command.DownloadsResume, str(item_id))
        return response.status_code == StatusCode.OK

    async def download_move_up(self, item_id: int) -> bool:
        """
        :param item_id: Identifier of the download to be moved up in the queue.
        :return: True if the operation was successful, False otherwise.
        """
        response = await self.send_command(Command.DownloadsMoveUp, str(item_id))
        return response.status_code == StatusCode.OK

    async def download_move_down(self, item_id: int) -> bool:
        """
        :param item_id: The unique identifier of the item to move down in the download list.
        :return: A boolean indicating whether the command to move the download down was successfully executed.
        """
        response = await self.send_command(Command.DownloadsMoveDown, str(item_id))
        return response.status_code == StatusCode.OK

    async def download_move_top(self, item_id: int) -> bool:
        """
        :param item_id: Identifier of the download to be moved to the top of the queue.
        :return: Boolean indicating whether the operation was successful.
        """
        response = await self.send_command(Command.DownloadsMoveTop, str(item_id))
        return response.status_code == StatusCode.OK

    async def download_move_bottom(self, item_id: int) -> bool:
        """
        Moves a download item to the bottom of the download queue.

        :param item_id: The identifier of the download item to be moved.
        :return: Returns True if the operation was successful, otherwise False.
        """
        response = await self.send_command(Command.DownloadsMoveBottom, str(item_id))
        return response.status_code == StatusCode.OK

    # Files methods

    async def get_files_count(self) -> int:
        """
        Asynchronously retrieves the count of files.

        :return: The count of files as an integer.
        """
        return await self.send_long_command(Command.FilesCount)

    async def get_files_list(self, start_index: int, end_index: int) -> List[FilesFileSet]:
        """
        :param start_index: The starting index for retrieving the list of files.
        :param end_index: The ending index for retrieving the list of files.
        :return: A list of FilesFileSet objects representing the retrieved files.
        """
        response = await self.send_list_command(Command.FilesList, str(start_index), str(end_index))
        result = []
        for file_set in response.list_items:
            result.append(FilesFileSet(file_set))

        return result

    async def download_file_from_files(self, file_name: str, item_id: int) -> bool:
        """
        :param file_name: The name of the file where the content will be saved.
        :param item_id: The identifier for the file to be downloaded.
        :return: True if the file was successfully downloaded, False otherwise.
        """
        with open(file_name, "wb") as stream:
            return await self.download_stream_from_files(stream, item_id)

    async def download_stream_from_files(self, stream: BinaryIO, item_id: int) -> bool:
        """
        :param stream: The binary stream where the downloaded file content will be written.
        :param item_id: The identifier of the file to be downloaded.
        :return: Returns True if the file was successfully downloaded, otherwise False.
        """
        response = await self.send_command(Command.FilesDownload, str(item_id))

        if response.status_code == StatusCode.OK:
            download_item = FilesDownloadItem(response.message)
            await self.send_command_without_response(Command.Continue)

            buffer = bytearray(4 * 1024)
            total_read = 0
            bytes_read = 0

            while total_read < download_item.file_size:
                bytes_to_read = download_item.file_size - total_read
                if bytes_to_read > len(buffer):
                    bytes_to_read = len(buffer)

                buffer = await self.read_binary(bytes_to_read)
                bytes_read = len(buffer)
                total_read += bytes_read
                stream.write(bytes(buffer[0:bytes_read]))

            response = self.get_response()

        return response.status_code == StatusCode.OK

    # Wish methods

    async def get_wish_count(self) -> int:
        """
        :return: The count of wishes as an integer received from sending the WishCount command.
        """
        return await self.send_long_command(Command.WishCount)

    async def get_wish_list(self, start_index: int, end_index: int) -> List[WishFileSet]:
        """
        :param start_index: The starting index for the wish list items to retrieve.
        :param end_index: The ending index for the wish list items to retrieve.
        :return: A list of WishFileSet objects representing the retrieved wish list items.
        """
        response = await self.send_list_command(Command.WishList, str(start_index), str(end_index))
        result = []
        for wish_set in response.list_items:
            result.append(WishFileSet(wish_set))

        return result

    async def download_from_wish(self, item_id: int) -> bool:
        """
        :param item_id: The unique identifier for the wish download request.
        :return: Boolean indicating whether the download operation was successful.
        """
        response = await self.send_command(Command.WishDownload, str(item_id))
        return response.status_code == StatusCode.OK

    # Upload methods

    async def upload_nzb_file(self, file_name: str) -> bool:
        """
        :param file_name: The path to the NZB file to be uploaded.
        :return: A boolean indicating whether the NZB file was successfully uploaded.
        """
        file_size = os.path.getsize(file_name)
        with open(file_name, "rb") as stream:
            return await self.upload_nzb_stream(file_name, stream, file_size)

    async def upload_nzb_stream(self, file_name: str, stream: BinaryIO, size: int) -> bool:
        """
        :param file_name: The name of the NZB file being uploaded.
        :param stream: A binary stream containing the contents of the NZB file.
        :param size: The size of the NZB file in bytes.
        :return: A boolean value indicating whether the upload operation was successful.
        """
        response = await self.send_command(Command.UploadNzbBinary, file_name, str(size))
        if response.status_code == StatusCode.OK:
            while True:
                while True:
                    buffer = stream.read(4096)
                    if len(buffer) == 0:
                        break
                    await self.write_binary(buffer)
                response = await self.get_response()
                return response.status_code == StatusCode.OK

        return False

    # Helper methods
    async def send_command(self, command: Command, arg1: str = "", arg2: str = "", arg3: str = "") -> Response:
        """
        :param command: The command to be sent to the external system.
        :param arg1: First argument to be appended to the command, optional.
        :param arg2: Second argument to be appended to the command, optional.
        :param arg3: Third argument to be appended to the command, optional.
        :return: A Response object containing the result from the external system.
        """
        command_line = command.value
        if arg1:
            command_line += f" {arg1}"
        if arg2:
            command_line += f" {arg2}"
        if arg3:
            command_line += f" {arg3}"

        await self.write_line_async(command_line)
        response = await self.read_line_async()
        return Response(response)

    async def send_list_command(self, command: Command, arg1: str = "", arg2: str = "") -> ListResponse:
        """
        :param command: The command to be sent, represented as a Command object.
        :param arg1: Optional string argument to append to the command.
        :param arg2: Optional string argument to append to the command.
        :return: A ListResponse object containing the parsed response data.
        """
        command_line = command.value
        if arg1:
            command_line += f" {arg1}"
        if arg2:
            command_line += f" {arg2}"

        await self.write_line_async(command_line)
        data = await self.read_line_async()
        result = ListResponse(data)
        if result.status_code == StatusCode.OK:
            while True:
                data = await self.read_line_async()
                if data == ".":
                    break
                result.add_list_item(data)

        return result

    async def send_long_command(self, command: Command, arg1="", arg2=""):
        """
        :param command: The command to be sent, represented as a Command object.
        :param arg1: An optional argument to be included in the command, defaults to an empty string.
        :param arg2: An optional second argument to be included in the command, defaults to an empty string.
        :return: An integer value parsed from the response message if the status code is OK, otherwise returns 0.
        """
        response = await self.send_command(command, arg1, arg2)
        if response.status_code == StatusCode.OK:
            return int(response.message.split()[0])
        return 0

    async def send_command_without_response(self, command: Command):
        """
        :param command: The command to be sent, represented as an instance of the Command class.
        :return: None. This method does not return a value.
        """
        await self.write_line_async(command.value)

    async def get_response(self) -> Response:
        """
        Reads a line asynchronously and returns a Response object containing the line read.

        :return: An instance of the Response class containing the data from the asynchronously read line.
        """
        response = await self.read_line_async()
        return Response(response)

    # Low level Helpers

    async def write_line_async(self, command: str):
        """
        :param command: The string command to write to the underlying writer, appended with a newline character.
        :return: None. This is an asynchronous method that writes the command and optionally executes a callback.
        """
        if self._writer:
            self._writer.write((command + '\n').encode('utf-8'))
            logging.debug(f"-> {command}")
            await self._writer.drain()
            if self._on_data_sent:
                if inspect.iscoroutinefunction(self._on_data_sent):
                    await asyncio.create_task(self._on_data_sent(command))
                else:
                    self._on_data_sent(command)

    async def read_line_async(self):
        """
        Reads a single line of data asynchronously using the reader and processes it.

        :return: A single line of data read from the reader, stripped of whitespace and decoded as a UTF-8 string.
        :rtype: str
        :raises AttributeError: If the `_reader` attribute is not set.
        """
        if self._reader:
            data = (await self._reader.readline()).decode('utf-8').strip()
            logging.debug(f"<- {data}")
            if self._on_data_received:
                if inspect.iscoroutinefunction(self._on_data_received):
                    await asyncio.create_task(self._on_data_received(data))
                else:
                    self._on_data_received(data)
            return data

    async def read_binary(self, bytes_to_read: int) -> bytes:
        """
        :param bytes_to_read: The number of bytes to read from the binary stream.
        :return: A bytes object containing the data read from the stream. Returns an empty bytes object if no reader is available.
        """
        if self._reader:
            return await self._reader.read(bytes_to_read)

        return b""

    async def write_binary(self, buffer: bytes, ) -> bool:
        """
        :param buffer: The binary data to write, passed as a bytes object.
        :return: A boolean value indicating whether the operation was successful. Returns True if the data was written successfully, otherwise False.
        """
        if self._writer:
            self._writer.write(buffer)
            await self._writer.drain()
            return True
        return False

    @staticmethod
    def get_auth_string(password: str, password_salt: str) -> str:
        """
        :param password: The original password string that needs to be hashed.
        :param password_salt: A salt string to be appended to the password for added security.
        :return: A hexadecimal string representation of the MD5 hash of the concatenated password and salt.
        """
        result = password + password_salt
        md5 = hashlib.md5()
        md5.update(result.encode('utf-8'))
        hash_bytes = md5.digest()
        return ''.join('{:02X}'.format(b) for b in hash_bytes)
