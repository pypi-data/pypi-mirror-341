from enum import Enum


class Command(Enum):
    Auth = "AUTH"
    Status = "STATUS"
    Bwl = "BWL"
    Pause = "PAUSE"
    ListServers = "LIST SERVERS"
    Update = "UPDATE"
    Save = "SAVE"
    Close = "CLOSE"

    ListGogs: str = "LIST GOGS"
    ListGroups: str = "LIST GROUPS"
    ListChildren: str = "LIST CHILDREN"
    ListChildrenDetails: str = "LIST CHILDRENDETAILS"
    ListFilters: str = "LIST FILTERS"

    FilterSetMinSize: str = "FILTER SETMINSIZE"
    FilterSetMaxSize: str = "FILTER SETMAXSIZE"
    FilterAddGroupFilter: str = "FILTER ADDGROUPFILTER"
    FilterSetAge = "FILTER SETAGE"
    FilterSetTextFilter = "FILTER SETTEXTFILTER"
    FilterHideOld = "FILTER HIDEOLD"
    FilterEnableFilters = "FILTER ENABLEFILTERS"
    FilterMarkOld = "FILTER MARKOLD"
    FilterMarkAllOld = "FILTER MARKOLD"
    FilterSetProfile = "FILTER SETPROFILE"
    FilterClear = "FILTER CLEAR"

    SearchLocal = "SEARCH LOCAL"
    SearchInternet = "SEARCH INTERNET"

    GroupLoad = "GROUP LOAD"
    GroupClear = "GROUP CLEAR"
    GroupDelete = "GROUP DELETE"

    LoadedCount = "LOADED COUNT"
    LoadedList = "LOADED LIST"
    LoadedSort = "LOADED SORT"
    LoadedClear = "LOADED CLEAR"
    LoadedFind = "LOADED FIND"
    LoadedDownload = "LOADED DOWNLOAD"
    LoadedGetNzb = "LOADED GETNZB"

    DownloadsCount = "DOWNLOADS COUNT"
    DownloadsLock = "DOWNLOADS LOCK"
    DownloadsUnlock = "DOWNLOADS UNLOCK"
    DownloadsList = "DOWNLOADS LIST"
    DownloadsSort = "DOWNLOADS SORT"
    DownloadsClear = "DOWNLOADS CLEAR"
    DownloadsFind = "DOWNLOADS FIND"
    DownloadsAssemble = "DOWNLOADS ASSEMBLE"
    DownloadsDelete = "DOWNLOADS DELETE"
    DownloadsPause = "DOWNLOADS PAUSE"
    DownloadsResume = "DOWNLOADS RESUME"
    DownloadsMoveUp = "DOWNLOADS MOVEUP"
    DownloadsMoveDown = "DOWNLOADS MOVEDOWN"
    DownloadsMoveTop = "DOWNLOADS MOVETOP"
    DownloadsMoveBottom = "DOWNLOADS MOVEBOTTOM"

    FilesCount = "FILES COUNT"
    FilesList = "FILES LIST"
    FilesDownload = "FILES DOWNLOAD"
    Continue = "300 CONTINUE"

    WishCount = "WISH COUNT"
    WishList = "WISH LIST"
    WishDownload = "WISH DOWNLOAD"

    UploadNzbBinary = "UPLOAD NZBBINARY"

    Quit = "QUIT"
