import datetime
import re
import typing

import pytz
from django.utils import timezone


def str_to_datetime(date_string, format='%Y-%m-%d %H:%M:%S'):
    """
    Support style:
    2018-12-07T06:24:24.000000
    2018-12-07T06:24:24Z
    2018-12-07 06:24:24
    ...
    """
    ds = re.findall(r'^(\d{4}-\d{2}-\d{2})[T\s](\d{2}:\d{2}:\d{2}).*$', date_string)
    if not ds:
        raise ValueError('Invalid datetime string: %s' % date_string)
    ds = ds[0]
    date_string = '%s %s' % (ds[0], ds[1])
    return datetime.datetime.strptime(date_string, format)


def to_aware_datetime(dt: typing.Union[str, datetime.datetime], tz=None):
    """
    Make an naive datetime using a given timezone(tz)

    Notice: tz if the timezone of dt, make sure they are matched
    """
    if dt is None:
        return
    if tz is None:
        tz = timezone.get_current_timezone()
    else:
        if isinstance(tz, str):
            tz = pytz.timezone(tz)
    if isinstance(dt, datetime.datetime):
        if timezone.is_aware(dt):
            return dt
        else:
            # Asia/Shanghai, same to settings
            return timezone.make_aware(dt)
    elif isinstance(dt, str):
        dt = str_to_datetime(dt)
        aware = timezone.make_aware(dt, timezone=tz)
        return aware
    raise ValueError


def humanize_datetime(dt: typing.Union[str, datetime.datetime], show_direction=True):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    if isinstance(dt, str):
        dt = to_aware_datetime(dt)
    delta = dt - timezone.datetime.now(tz=timezone.get_current_timezone())
    a_day = 86400
    an_hour = 3600
    a_minute = 60
    timetot = ''
    total_secs = secs = delta.total_seconds()
    if secs > 0:
        direction = '后'
    elif secs < 0:
        direction = '前'
        total_secs = -total_secs
        secs = -secs
    else:
        return '刚刚'
    if secs > a_day:  # 60sec * 60min * 24hrs
        days = int(secs // a_day)
        # timetot += "{} {}".format(int(days), _('days'))
        timetot += '%(num)s天' % {'num': days}
        secs = secs - days * a_day

    if secs > an_hour:
        hrs = int(secs // an_hour)
        # timetot += " {} {}".format(int(hrs), _('hours'))
        timetot += ' '
        timetot += '%(num)s小时' % {'num': hrs}
        secs = secs - hrs * an_hour

    if secs > a_minute and total_secs < a_day:
        mins = int(secs // a_minute)
        timetot += ' '
        timetot += '%(num)s分钟' % {'num': mins}
        secs = secs - mins * a_minute

    if secs > 0 and total_secs < an_hour:
        secs = int(secs)
        timetot += ' '
        timetot += '%(num)s秒' % {'num': secs}

    if not timetot and secs == 0:
        timetot = '刚刚'
    else:
        if show_direction:
            timetot += ' %s' % direction
    return timetot


def humanize_datetime_simple(dt: typing.Union[str, datetime.datetime], show_direction=True):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    if isinstance(dt, str):
        dt = to_aware_datetime(dt)
    delta = dt - timezone.datetime.now(tz=timezone.get_current_timezone())
    a_day = 86400
    an_hour = 3600
    a_minute = 60
    timetot = ''
    total_secs = secs = delta.total_seconds()
    if secs > 0:
        direction = '后'
    elif secs < 0:
        direction = '前'
        total_secs = -total_secs
        secs = -secs
    else:
        return '刚刚'
    if secs > a_day:  # 60sec * 60min * 24hrs
        days = int(secs // a_day)
        # timetot += "{} {}".format(int(days), _('days'))
        timetot += '%(num)s天' % {'num': days}
        secs = secs - days * a_day

    if secs > an_hour:
        hrs = int(secs // an_hour)
        # timetot += " {} {}".format(int(hrs), _('hours'))
        timetot += ' '
        timetot += '%(num)s小时' % {'num': hrs}
        secs = secs - hrs * an_hour

    if secs > a_minute and total_secs < a_day:
        mins = int(secs // a_minute)
        timetot += ' '
        timetot += '%(num)s分钟' % {'num': mins}
        secs = secs - mins * a_minute

    elif secs > 0 and total_secs < an_hour:
        secs = int(secs)
        timetot += ' '
        timetot += '%(num)s秒' % {'num': secs}

    if not timetot and secs == 0:
        timetot = '刚刚'
    else:
        if show_direction:
            timetot += ' %s' % direction
    return timetot
