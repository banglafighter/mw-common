import calendar
from datetime import datetime, date, timedelta
import time
from .mw_common_data import DateData
from .mw_exception import MwException


class DateUtil:

    @classmethod
    def format_date(cls, date_data, date_format: str = "%d/%m/%Y"):
        return date_data.strftime(date_format)

    @classmethod
    def format_datetime(cls, datetime_data: datetime, datetime_format: str = "%d/%m/%Y %H:%M:%S") -> str:
        if datetime_data is None:
            raise MwException("datetime_data cannot be None")
        return datetime_data.strftime(datetime_format)

    @classmethod
    def string_to_datetime(cls, string_date: str, date_format: str = "%d/%m/%Y %H:%M:%S"):
        date_time_data = datetime.strptime(string_date, date_format)
        if date_time_data:
            return date_time_data
        return None

    @classmethod
    def string_to_date(cls, string_date: str, date_format: str = "%d/%m/%Y"):
        date_time_data = cls.string_to_datetime(string_date, date_format)
        if date_time_data:
            return date_time_data.date()
        return None

    @classmethod
    def format_today(cls, date_format: str = "%d/%m/%Y"):
        today = datetime.today()
        return today.strftime(date_format)

    @classmethod
    def start_of_day(cls, string_date: str | date | datetime = None, date_format: str = "%d/%m/%Y", send_string: bool = False):
        if not string_date:
            string_date = cls.format_today(date_format=date_format)

        if isinstance(string_date, date):
            string_date = cls.format_date(string_date, date_format=date_format)

        if isinstance(string_date, datetime):
            string_date = cls.format_datetime(string_date, datetime_format=date_format)

        starting_datetime = f"{string_date} 00:00:00"

        if send_string:
            return starting_datetime

        return cls.string_to_datetime(string_date=starting_datetime, date_format=f"{date_format} %H:%M:%S")

    @classmethod
    def end_of_day(cls, string_date: str | date | datetime = None, date_format: str = "%d/%m/%Y", send_string: bool = False):
        if not string_date:
            string_date = cls.format_today(date_format=date_format)

        if isinstance(string_date, date):
            string_date = cls.format_date(string_date, date_format=date_format)

        if isinstance(string_date, datetime):
            string_date = cls.format_datetime(string_date, datetime_format=date_format)

        starting_datetime = f"{string_date} 23:59:59"

        if send_string:
            return starting_datetime
        return cls.string_to_datetime(string_date=starting_datetime, date_format=f"{date_format} %H:%M:%S")

    @classmethod
    def start_of_month(cls, date_object: date = None) -> date:
        if not date_object:
            date_object = date.today()
        return date(date_object.year, date_object.month, 1)

    @classmethod
    def end_of_month(cls, date_object: date = None) -> date:
        if not date_object:
            date_object = date.today()
        last_day = calendar.monthrange(date_object.year, date_object.month)[1]
        return date(date_object.year, date_object.month, last_day)

    @classmethod
    def get_weekday(cls):
        today = date.today()
        return today.strftime("%A")

    @classmethod
    def get_db_datetime(cls):
        return datetime.now()

    @classmethod
    def get_db_date(cls):
        return date.today()

    @classmethod
    def get_timestamp(cls):
        return int(time.time() * 1000)

    @classmethod
    def get_date_components(cls, input_date: date = None) -> DateData:
        if not input_date:
            input_date = date.today()
        date_data = DateData(
            year=input_date.year,
            month=input_date.month,
            yearShort=int(input_date.strftime("%y")),
            monthName=input_date.strftime("%B"),
            monthShort=input_date.strftime("%b"),
            day=input_date.day,
            weekday=input_date.strftime("%A"),
            dayOfYear=input_date.strftime("%j"),
            weekOfYear=input_date.strftime("%W")
        )
        return date_data

    @classmethod
    def get_days(cls, to_date: date | datetime, from_date: date | datetime | None = None):
        if to_date is None:
            raise MwException("to_date cannot be None")

        if isinstance(to_date, datetime):
            to_date = to_date.date()
        if from_date is None:
            from_date = date.today()
        elif isinstance(from_date, datetime):
            from_date = from_date.date()
        return (from_date - to_date).days

    @classmethod
    def add_days(cls, base_date: date | datetime, days: int) -> date | datetime:
        if base_date is None:
            raise MwException("base_date cannot be None")
        return base_date + timedelta(days=days)

    @classmethod
    def subtract_days(cls, base_date: date | datetime, days: int) -> date | datetime:
        return cls.add_days(base_date, -days)

    @classmethod
    def today(cls):
        return date.today()
