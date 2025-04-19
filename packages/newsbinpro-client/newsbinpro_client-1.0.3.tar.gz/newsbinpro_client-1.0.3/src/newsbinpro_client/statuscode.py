from enum import IntEnum


class StatusCode(IntEnum):
    """
    StatusCode is an enumerated type (IntEnum) representing various status codes and error codes.

    This enum is used to define internal codes, Newsbin operational codes, and errors that are encountered during executions.
    """
    # Internal Codes
    ParseError = 90  #: The operation encountered a parse error.

    # Newsbin Operational Codes
    OK = 200  #: The operation was successful.
    StatusBwLimiterOn = 251  #: The bandwidth limiter is enabled.
    StatusBwLimiterOff = 252  #: The bandwidth limiter is disabled.
    StatusPauseOn = 253  #: The pause mode is enabled.
    StatusPauseOff = 254  #: The pause mode is disabled.
    StatusPostData = 300  #: Indicates new data for posting.

    # Error Codes
    ErrorNotEnoughParams = 401  #: Insufficient parameters were provided for the operation.
    ErrorAgeMinGreaterThanMax = 402  #: The minimum age exceeds the maximum age.
    ErrorGroupListRange = 403  #: The group list range is invalid.
    ErrorRangeMinGreaterThanMax = 404  #: The range's minimum value exceeds the maximum value.
    ErrorRangeExceeded = 405  #: The range exceeds allowable limits.
    ErrorSortColumnExceeded = 406  #: The sort column exceeds valid limits.
    ErrorGroupListNoGroup = 407  #: Missing group in the group list.
    ErrorUpdateGroupMissing = 408  #: The update operation is missing a group.
    ErrorUpdateGroupNotFound = 409  #: The specified update group was not found.
    ErrorFindInvalidSearchString = 410  #: The search string provided is invalid.
    ErrorUploadMissingFileName = 411  #: The upload operation is missing a file name.
    ErrorUploadUnableToSave = 412  #: Failure occurred while saving an uploaded file.
    ErrorAuthNoPasswordSet = 413  #: No password is set for authentication.
    ErrorAuthNotRegistered = 414  #: The user is not registered.
    ErrorUnregistered = 415  #: An unregistered user attempted an operation.
    ErrorVarFormatError = 416  #: A variable format error occurred.
    ErrorVarVariableNotFound = 417  #: A specified variable was not found.
    ErrorVarUnableToSet = 418  #: Failed to set a specified variable.
    ErrorUnableToSaveConfig = 419  #: Unable to save configuration changes.
    ErrorUploadMissingFileSize = 420  #: The upload is missing the file size.
    ErrorUploadNoAutoload = 421  #: No autoload is set for this upload operation.
    ErrorDownloadNoFile = 430  #: No file exists for the specified download.
    ErrorDownloadIncomplete = 431  #: The download process was incomplete.
    ErrorFilterNotFound = 440  #: The specified filter was not found.
    AuthNeedAuth = 480  #: Authentication is required for this operation.
    ErrorUnimplemented = 500  #: The operation is not yet implemented.
