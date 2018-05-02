#!/usr/bin/env python3
import csv
import re
import sys

RX_YEAR = re.compile('^(?P<year>19[789][0-9]):$')
RX_TYPE = re.compile('^(?P<type>Boxed Sets|Hardcovers|Adventures|Accessories):$')
RX_TAG = re.compile('(?P<tag>D&D|AQ|BR|DL|DS|FR|GH|LNK|M2E|PS|RL|SJ)$')
RX_CODE = re.compile('^(?P<code>[A-Z]+[0-9-]+)')

year = None
_type = None

records = []


def setting_code_to_setting(setting_code):
    if setting_code == 'AQ':
        return 'Al-Qadim'
    elif setting_code == 'BR':
        return 'Birthright'
    elif setting_code == 'DL':
        return 'Dragonlance'
    elif setting_code == 'DS':
        return 'Dark Sun'
    elif setting_code == 'FR':
        return 'Forgotten Realms'
    elif setting_code == 'GH':
        return 'Greyhawk'
    elif setting_code == 'LNK':
        return 'Lankhmar'
    elif setting_code == 'M2E':
        return 'Mystara (2E)'
    elif setting_code == 'PS':
        return 'Planescape'
    elif setting_code == 'RL':
        return 'Ravenloft'
    elif setting_code == 'SJ':
        return 'Spelljammer'
    elif setting_code == '':
        return ''
    else:
        raise Exception('bad setting code: "{}"'.format(setting_code))


def singularize_type(_type):
    if _type == 'accessories':
        return 'accessory'
    elif _type == 'adventures':
        return 'adventure'
    elif _type == 'boxed sets':
        return 'boxed set'
    elif _type == 'hardcovers':
        return 'hardcover'
    else:
        raise Exception('bad type: ' + _type)


for line in sys.stdin:
    s = line.rstrip()
    if not s:
        continue
    match = RX_YEAR.search(s)
    if match:
        year = match.groupdict()['year']
        continue
    match = RX_TYPE.search(s)
    if match:
        _type = match.groupdict()['type'].lower()
        continue
    match = RX_TAG.search(s)
    system = 'AD&D'
    setting_code = ''
    if match:
        title = RX_TAG.sub('', s)
        if match.groupdict()['tag'] == 'D&D':
            system = 'D&D'
        else:
            setting_code = match.groupdict()['tag']
    else:
        title = s
    match = RX_CODE.search(title)
    if match:
        code = match.groupdict()['code']
        title = RX_CODE.sub('', title)
    else:
        code = ''
    title = title.strip()
    records.append([year, title, code, singularize_type(_type), system, setting_code_to_setting(setting_code)])

csv_writer = csv.writer(sys.stdout)
csv_writer.writerow(['year', 'title', 'code', 'type', 'system', 'setting'])
for record in records:
    csv_writer.writerow(record)
