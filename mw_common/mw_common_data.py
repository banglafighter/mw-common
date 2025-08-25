from dataclasses import dataclass


@dataclass(kw_only=True)
class DateData:
    day: int
    month: int
    monthName: str
    monthShort: str
    year: int
    yearShort: int
    weekday: str
    dayOfYear: str
    weekOfYear: str
