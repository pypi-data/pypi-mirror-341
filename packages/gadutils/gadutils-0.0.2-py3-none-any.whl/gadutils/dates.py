import calendar
import datetime
import enum


class Format(str, enum.Enum):
    year = "%Y"
    month = "%m"
    month_short = "%b"
    month_full = "%B"
    day = "%d"
    day_short = "%a"
    day_full = "%A"
    hour = "%H"
    minute = "%M"
    second = "%S"
    microsecond = "%f"
    timezone = "%z"

    @classmethod
    def iso(cls) -> str:
        return "{year}-{month}-{day}T{hour}:{minute}:{second}.{microsecond}{timezone}".format(
            year=cls.year.value,
            month=cls.month.value,
            day=cls.day.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
            microsecond=cls.microsecond.value,
            timezone=cls.timezone.value,
        )

    @classmethod
    def short(cls) -> str:
        return "{year}-{month}-{day}".format(
            year=cls.year.value,
            month=cls.month.value,
            day=cls.day.value,
        )

    @classmethod
    def full(cls) -> str:
        return "{day_short}, {day} {month_short} {year} {hour}:{minute}:{second}".format(
            day_short=cls.day_short.value,
            day=cls.day.value,
            month_short=cls.month_short.value,
            year=cls.year.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
        )

    @classmethod
    def human(cls) -> str:
        return "{day} {month_full} {year}".format(
            day=cls.day.value,
            month_full=cls.month_full.value,
            year=cls.year.value,
        )

    @classmethod
    def time(cls) -> str:
        return "{hour}:{minute}:{second}".format(
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
        )

    @classmethod
    def us(cls) -> str:
        return "{month}/{day}/{year}".format(
            month=cls.month.value,
            day=cls.day.value,
            year=cls.year.value,
        )

    @classmethod
    def eu(cls) -> str:
        return "{day}/{month}/{year}".format(
            day=cls.day.value,
            month=cls.month.value,
            year=cls.year.value,
        )

    @classmethod
    def rfc2822(cls) -> str:
        return "{day_short}, {day} {month_short} {year} {hour}:{minute}:{second} {timezone}".format(
            day_short=cls.day_short.value,
            day=cls.day.value,
            month_short=cls.month_short.value,
            year=cls.year.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
            timezone=cls.timezone.value,
        )

    @classmethod
    def rfc3339(cls) -> str:
        return "{year}-{month}-{day}T{hour}:{minute}:{second}{timezone}".format(
            year=cls.year.value,
            month=cls.month.value,
            day=cls.day.value,
            hour=cls.hour.value,
            minute=cls.minute.value,
            second=cls.second.value,
            timezone=cls.timezone.value,
        )


def now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


def midnight() -> datetime:
    return now().replace(hour=0, minute=0, second=0, microsecond=0)


def today() -> datetime.date:
    return now().date()


def tostring(date: datetime.datetime, fmt: str) -> str:
    return date.strftime(fmt)


def fromstring(date: str, fmt: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, fmt)


def before(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date < comparison


def after(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date > comparison


def include(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date <= now() <= comparison.date()


def same(date: datetime.datetime, comparison: datetime.datetime) -> bool:
    return date == comparison


def diff(date: datetime.datetime, comparison: datetime.datetime) -> datetime.timedelta:
    return date - comparison


def age(date: datetime.datetime) -> int:
    return (now() - date).days // 365


def calendarmonthname(date: datetime.datetime) -> str:
    return calendar.month_name[date.month].lower()


def calendarmonthabbr(date: datetime.datetime) -> str:
    return calendar.month_abbr[date.month].lower()


def calendardayname(date: datetime.datetime) -> str:
    return calendar.day_name[date.weekday()].lower()


def calendardayabbr(date: datetime.datetime) -> str:
    return calendar.day_abbr[date.weekday()].lower()


def calendarmonthrange(date: datetime.datetime) -> int:
    return calendar.monthrange(date.year, date.month)[1]


def formatiso(date: datetime.datetime) -> str:
    return tostring(date, Format.iso())


def formatshort(date: datetime.datetime) -> str:
    return tostring(date, Format.short())


def formatfull(date: datetime.datetime) -> str:
    return tostring(date, Format.full())


def formathuman(date: datetime.datetime) -> str:
    return tostring(date, Format.human())


def formattime(date: datetime.datetime) -> str:
    return tostring(date, Format.time())


def formatus(date: datetime.datetime) -> str:
    return tostring(date, Format.us())


def formateu(date: datetime.datetime) -> str:
    return tostring(date, Format.eu())


def formatrfc2822(date: datetime.datetime) -> str:
    return tostring(date, Format.rfc2822())


def formatrfc3339(date: datetime.datetime) -> str:
    return tostring(date, Format.rfc3339())


def start(date: datetime.datetime) -> datetime.datetime:
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def end(date: datetime.datetime) -> datetime.datetime:
    return date.replace(hour=23, minute=59, second=59, microsecond=999999)


def weekend(date: datetime.datetime) -> bool:
    return date.weekday() >= 5
