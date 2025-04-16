from dahua.utils.logger import logger


class DahuaRequestError(Exception):
    """Exception raised for request errors."""


# ========== Dahua Request Errors ==========
class DahuaErrorCodeNotSet(DahuaRequestError):
    """Error code not set."""


class DahuaInterfaceNotFound(DahuaRequestError):
    """Interface not found."""


class DahuaMethodNotFound(DahuaRequestError):
    """Method not found."""


class DahuaRequestInvalid(DahuaRequestError):
    """Request invalid."""


class DahuaRequestInvalidParam(DahuaRequestError):
    """Request invalid parameter."""


class DahuaSessionInvalid(DahuaRequestError):
    """Session invalid."""


class DahuaInvalidCredentials(DahuaRequestError):
    """User or password not valid."""


class DahuaInBlackList(DahuaRequestError):
    """User in black list."""


class DahuaHasBeenUsed(DahuaRequestError):
    """User has been used."""


class DahuaHasBeenLocked(DahuaRequestError):
    """User has been locked."""


class DahuaBusy(DahuaRequestError):
    """Device is busy."""


def code_to_exception(code: int) -> type[DahuaRequestError]:
    """Convert error code to exception class."""
    if code == 268632085:
        return DahuaInvalidCredentials
    if code == 268632081:
        return DahuaHasBeenLocked
    if code == 268959743:
        return DahuaErrorCodeNotSet
    if code == 268632064:
        return DahuaInterfaceNotFound
    if code == 268894210:
        return DahuaMethodNotFound
    if code == 268894209:
        return DahuaRequestInvalid
    if code == 268894211:
        return DahuaRequestInvalidParam
    if code == 28763750:
        return DahuaSessionInvalid
    if code == 268632073:
        return DahuaInBlackList
    if code == 268632074:
        return DahuaHasBeenUsed
    if code == 268632075:
        return DahuaBusy

    logger.warning(f"Unknown error code: {code}")
    return DahuaRequestError
