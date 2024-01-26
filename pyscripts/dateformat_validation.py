from datetime import datetime

class DateFormatValidator:
    def __init__(self, date_format):
        self.date_format = date_format

    def validate(self, date_str):
        try:
            datetime.strptime(date_str, self.date_format)
            return True
        except ValueError:
            return False