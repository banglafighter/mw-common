from datetime import datetime


class DateUtil:

    @classmethod
    def format_date(cls, date_data, date_format: str = "%d/%m/%Y"):
        return date_data.strftime(date_format)

    @classmethod
    def string_to_datetime(cls, string_date: str, date_format: str = "%d/%m/%Y %H:%M:%S"):
        date_time_data = datetime.strptime(string_date, date_format)
        if date_time_data:
            return date_time_data
        return None

    @classmethod
    def format_today(cls, date_format: str = "%d/%m/%Y"):
        today = datetime.today()
        return today.strftime(date_format)

    @classmethod
    def start_of_day(cls, string_date: str = None, date_format: str = "%d/%m/%Y"):
        if not string_date:
            string_date = cls.format_today(date_format=date_format)
        starting_datetime = f"{string_date} 00:00:00"
        return cls.string_to_datetime(string_date=starting_datetime, date_format=f"{date_format} %H:%M:%S")

    @classmethod
    def end_of_day(cls, string_date: str = None, date_format: str = "%d/%m/%Y"):
        if not string_date:
            string_date = cls.format_today(date_format=date_format)
        starting_datetime = f"{string_date} 23:59:59"
        return cls.string_to_datetime(string_date=starting_datetime, date_format=f"{date_format} %H:%M:%S")
