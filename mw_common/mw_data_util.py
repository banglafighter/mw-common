class DataUtil:

    @staticmethod
    def dict_value(data: dict, key: str, default=None):
        if not data or not key:
            return default
        elif key in data:
            return data[key]
        return default

    @staticmethod
    def round_amount(amount, after_point=3):
        if not amount:
            return amount
        return round(amount, after_point)

    @staticmethod
    def parse_float(value):
        if value is None:
            return value
        return float(str(value))

    @staticmethod
    def parse_int(value):
        if value is None:
            return value
        return int(str(value))

    @staticmethod
    def percentage_value(amount, percentage):
        if amount is None or percentage is None:
            return amount
        return (amount * percentage) / 100
