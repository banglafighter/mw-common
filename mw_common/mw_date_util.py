

class DateUtil:

    @classmethod
    def date_to_string(cls, date_data, date_format: str = "%d/%m/%Y"):
        return date_data.strftime(date_format)