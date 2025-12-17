import re
from ..mw_exception import MwException


class ISO8601Time:
    _PATTERN = re.compile(
        r'^P'
        r'(?:(\d+)Y)?'
        r'(?:(\d+)M)?'
        r'(?:(\d+)W)?'
        r'(?:(\d+)D)?'
        r'(?:T'
        r'(?:(\d+)H)?'
        r'(?:(\d+)M)?'
        r'(?:(\d+)S)?'
        r')?$'
    )

    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    def __init__(self, duration: str):
        if not isinstance(duration, str):
            raise MwException("Duration must be a string")

        self.duration = duration
        self._parse()

    def _parse(self) -> None:
        match = self._PATTERN.match(self.duration)
        if not match:
            raise MwException(f"Invalid ISO-8601 duration: {self.duration}")

        (years, months, weeks, days, hours, minutes, seconds) = match.groups()
        self.years = int(years) if years else 0
        self.months = int(months) if months else 0
        self.weeks = int(weeks) if weeks else 0
        self.days = int(days) if days else 0
        self.hours = int(hours) if hours else 0
        self.minutes = int(minutes) if minutes else 0
        self.seconds = int(seconds) if seconds else 0

    def human_readable(self, hour: str = None, minute: str = None, second: str = None) -> str:
        parts = []

        if self.weeks:
            parts.append(f"{self.weeks} week{'s' if self.weeks > 1 else ''}")
        if self.days:
            parts.append(f"{self.days} day{'s' if self.days > 1 else ''}")

        if self.hours:
            label = f" hour{'s' if self.hours > 1 else ''}"
            if hour:
                label = hour
            parts.append(f"{self.hours}{label}")

        if self.minutes:
            label = f" minute{'s' if self.minutes > 1 else ''}"
            if minute:
                label = minute
            parts.append(f"{self.minutes}{label}")

        if self.seconds:
            label = f" second{'s' if self.seconds > 1 else ''}"
            if second:
                label = second
            parts.append(f"{self.seconds}{label}")

        return " ".join(parts) if parts else ""

    def minute(self) -> int:
        if self.years or self.months:
            raise MwException("Years and months cannot be safely converted to minutes")

        total = 0
        total += self.seconds // 60
        total += self.minutes
        total += self.hours * 60
        total += self.days * 1440
        total += self.weeks * 10080

        return total

    def second(self) -> int:
        if self.years or self.months:
            raise MwException("Years and months cannot be safely converted to seconds")

        total = 0
        total += self.seconds
        total += self.minutes * 60
        total += self.hours * 3600
        total += self.days * 86400
        total += self.weeks * 604800

        return total

    def __str__(self) -> str:
        return self.human_readable()

    def __repr__(self) -> str:
        return f"<ISO8601Time {self.duration}>"
