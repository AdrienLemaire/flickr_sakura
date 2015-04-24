# -*- coding: utf-8 -*-
import re
from datetime import datetime


RE_TS = re.compile('(\d{13}).jpg')
RE_DT = re.compile('(\d{8})[_-](\d{6})')
DATE_STR = lambda d: d.strftime('%Y-%m-%d %H:%M:%S')


def check_timestamp(title):
    matchs = RE_TS.findall(title)
    if not matchs:
        return False
    ts = int(RE_TS.findall(title)[0]) / 1000.0
    return DATE_STR(datetime.fromtimestamp(ts))
 

def check_date_time(title):
    matchs = RE_DT.findall(title)
    if not matchs:
        return False
    return DATE_STR(datetime.strptime('_'.join(matchs), '%Y%m%d_%H%M%S'))


def find_date_taken(title):
    checks = [k for k in globals().keys() if k.startswith('check_')]
    date_taken = None
    while not date_taken or not checks:
        date_taken = globals()[checks.pop()](title)
    return date_taken
