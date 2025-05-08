from datetime import timedelta
from models.date import Date


class DateService:
    def __init__(self, current_date):
        self._current_date = current_date
        self.__date_formated = Date.DATE_FORMAT
        self.default_date = None
        self.index_request_date = None
        self.yields_request_date = None

    def __transform_date(self, days_diff, date_format=None):
        if date_format:
            past_day = self._current_date - timedelta(days=days_diff)
            return past_day.strftime(date_format)
        return self._current_date + timedelta(days=days_diff)
    
    def set_default_date(self):
        return self.__transform_date(
            days_diff=Date.default_days_delay
        )

    def set_index_request_date(self):
        return self.__transform_date(
            days_diff=Date.inflation_days_delay,
            date_format=self.__date_formated
        )

    def set_yields_request_date(self):
        return self.__transform_date(
            days_diff=Date.yields_days_delay,
            date_format=self.__date_formated
        )
