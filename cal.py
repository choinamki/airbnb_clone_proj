import calendar


class Calendar(calendar.Calendar):

    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ('Mon', 'Tue', 'Wed', 'Fri', 'Sat', 'Sun')
        self.months = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
                       'August', 'September', 'October', 'November', 'December')

    def get_days(self):
        days = list()
        weeks = self.monthdays2calendar(self.year, self.month)

        for week in weeks:
            for day, _ in week:
                days.append(day)
        return days

    def get_month(self):
        return self.months[self.month - 1]



new_cal = Calendar(2019, 11)
new_cal.get_days()
