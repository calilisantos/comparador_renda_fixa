from datetime import timedelta


class Date:
    def __init__(self, current_date):
        self._current_date = current_date
    def transform_date(self, days_diff, date_format=None):
        if date_format:
            past_day = self._current_date - timedelta(days=days_diff)
            return past_day.strftime(date_format)
        return self._current_date + timedelta(days=days_diff)
