from datetime import datetime, timedelta, timezone
from typing import Optional

_UTC = timezone(timedelta(hours=0.0))


def get_now_utc() -> datetime:
    """
    Returns the current time in UTC
    """
    return datetime.now(tz=_UTC)


def get_datetime_as_isotutc(dt: datetime) -> str:
    """
    Converts a datetime to UTC and then to the correct ISOT format for the API.
    Adds UTC timezone if missing.
    """
    if dt.tzinfo is None:
        print(f"Assuming naive datetime {dt} is in UTC.")
        dt = dt.replace(tzinfo=_UTC)
    dt_utc = dt.astimezone(tz=_UTC)
    return dt_utc.isoformat().replace("+00:00", "Z")


def sanitize_datetime(dt: datetime | str) -> str:
    """
    Sanitizes de datetime or string to be compatible with the Astrolabe API
    If no timezone is supplied, UTC is assumed.

    Strings are assumed to be ISO8601 format.
    """
    if isinstance(dt, datetime):
        return get_datetime_as_isotutc(dt)
    elif isinstance(dt, str):
        if dt[-1] == "Z":
            dt = dt.replace("Z", "+00:00")
        return get_datetime_as_isotutc(datetime.fromisoformat(dt))
    else:
        raise ValueError(
            f"Invalid type for datetime '{type(dt)}'. Please use either a datetime or a ISO8601-format date string"
        )


def parse_bool(b: Optional[str]) -> bool | None:
    if b is None:
        return None

    if b.lower() in ("true", "t", "yes", "on"):
        return True
    elif b.lower() in ("false", "f", "no", "off"):
        return False
    else:
        raise ValueError(f"Invalid boolean value '{b}'. Cannot be parsed.")


def parse_int(i: Optional[str]) -> int | None:
    if i is None:
        return None
    else:
        return int(i)


def parse_float(f: Optional[str]) -> float | None:
    if f is None:
        return None
    else:
        return float(f)
