from datetime import datetime, timezone
from utilities_pufm.enums.enums import TimeTypes

def get_current_time(time_type: str = TimeTypes.YMD.value) -> str:
    """
    Gets the current time formatted as a string.

    This function retrieves the current date and time, formats it according to
    the provided `time_type` string, and returns it as a string. The default
    format corresponds to the `YMD` value from the `TimeTypes` enumeration.

    Args:
        time_type (str): A format string specifying how to format the date and time.
            The default is `TimeTypes.YMD.value`, typically representing a format like
            'YYYY-MM-DD'. Ensure the string conforms to Python's `strftime` directives.

    Returns:
        str: The current date and time formatted as a string according to the given format.

    Raises:
        ValueError: If the provided `time_type` is not a valid `strftime` format string.

    Example:
        >>> from utilities.time.enums import TimeTypes
        >>> get_current_time(TimeTypes.HMS.value)
        '12:34:56'
    """
    return datetime.now().strftime(time_type)

def get_time_from_seconds(seconds: int, time_type: str = TimeTypes.HMS.value) -> str:
    
    # return str(timedelta(seconds=seconds))
    return datetime.fromtimestamp(seconds, tz=timezone.utc).strftime(time_type)