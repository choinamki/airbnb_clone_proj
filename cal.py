from django.utils import timezone
import calendar


class Day:
    def __init__(self, number, month, year, past):
        self.number = number
        self.past = past
        self.month = month
        self.year = year

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):

    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
        self.months = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
                       'August', 'September', 'October', 'November', 'December')

    def get_days(self):
        days = list()
        weeks = self.monthdays2calendar(self.year, self.month)

        for week in weeks:
            for day, _ in week:
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month == self.month:
                    if day <= today:
                        past = True
                new_day = Day(number=day, past=past, month=self.month, year=self.year)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]


new_cal = Calendar(2019, 11)
new_cal.get_days()
