import jdatetime
from django.utils import timezone
from django import template
from datetime import date

register = template.Library()

@register.simple_tag
def shamsi_year():
    PERSIAN_DIGITS = {
        "0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴",
        "5": "۵", "6": "۶", "7": "۷", "8": "۸", "9": "۹",
    }
    today = date.today()
    jdate = jdatetime.date.fromgregorian(date=today)
    year = str(jdate.year)
    return ''.join(PERSIAN_DIGITS.get(ch, ch) for ch in year)

@register.filter
def to_jalali(value, fmt="%Y/%m/%d"):
    if not value:
        return ""
    jdate = jdatetime.datetime.fromgregorian(datetime=value)

    value = timezone.localtime(value)

    return jdate.strftime(fmt)