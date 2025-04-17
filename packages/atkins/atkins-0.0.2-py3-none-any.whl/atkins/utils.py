from datetime import timedelta


def get_timeduration(duration_str: str) -> timedelta:
    """
    Parse duration string to a timedelta object.
    Supported formats: 1m (minute), 2h (hour), 3d (day), 4w (week), 5y (year)
    :param duration_str: Duration string (e.g. "1m", "2h", "3d", "4w", "5y")
    :return: A timedelta object representing the parsed duration
    :raises ValueError: If the input string format is invalid
    """
    if not duration_str or not isinstance(duration_str, str):
        raise ValueError("Invalid duration string provided.")

    # Define multipliers for each unit
    multipliers = {
        "m": timedelta(minutes=1),
        "h": timedelta(hours=1),
        "d": timedelta(days=1),
        "w": timedelta(weeks=1),
        "y": timedelta(days=365)  # Approximate a year as 365 days
    }

    # Extract the numeric value and unit
    try:
        value = int(duration_str[:-1])  # Strip the last character (unit) and convert to integer
        unit = duration_str[-1]  # Extract the unit
    except (ValueError, IndexError):
        raise ValueError("Duration string must be in the format '<number><unit>' (e.g., '1m', '2h', '3d').")

    # Calculate timedelta based on unit
    if unit in multipliers:
        return value * multipliers[unit]
    else:
        raise ValueError(
            f"Unsupported duration unit '{unit}'. Supported units: 'm' (minute), 'h' (hour), 'd' (day), 'w' (week), 'y' (year).")
