from dataclasses import dataclass
from datetime import datetime

@dataclass
class RawCandle:

    # Datetime in UTC
    # |
    # |
    # v
    dt: datetime # <-- In UTC
    # ^
    # |
    # |
    # In UTC

    o: float
    h: float
    l: float
    c: float
