#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os.path
from pprint import pprint

FILE_PATH = os.path.join(os.path.dirname(__file__), 'csv_files')


def get_csv_paths(path=FILE_PATH):
    if not os.path.exists(path):
        raise ValueError('CSV files path does not exist, please make sure {path} exists'.format(path=path))
    for _, _, files in os.walk(path):
        return sorted([(file, os.path.join(path, file)) for file in files])


WEEK_DAYS = ('mon', 'tue', 'wed', 'thu', 'fri')


def get_days(spec):
    if '-' not in spec and spec not in WEEK_DAYS:
        return
    if spec in WEEK_DAYS:
        yield spec
        return
    start, end = spec.split('-', 1)
    if start not in WEEK_DAYS or end not in WEEK_DAYS:
        return
    in_range = False
    for day in WEEK_DAYS:
        if day == start:
            in_range = True
        if in_range:
            yield day
        if day == end:
            if not in_range:
                raise ValueError('Day spec {spec}, does not contain starting range'.format(spec=spec))
            in_range = False


def read_csv_file(csv_file_path):
    with open(csv_file_path) as file:
        file_lines = file.readlines()
        if len(file_lines) != 2:
            raise ValueError(
                'CSV {csv_file_path} does not follow training set format'.format(csv_file_path=csv_file_path))
        spec_line, data_line = file_lines
    spec, data = spec_line.strip().split(','), data_line.strip().split(',')
    if len(spec) != len(data):
        raise ValueError('CSV {csv_file_path} contains different column lengths'.format(csv_file_path=csv_file_path))
    return zip(spec, data)


def extract_week_information(entries):
    week = dict()
    description = None
    for spec, data in entries:
        maybe_days = list(get_days(spec))
        if maybe_days:
            for day in maybe_days:
                if day in week:
                    raise ValueError(
                        'Entries {entries} contains duplicate data for day {day}'.format(entries=entries, day=day))
                try:
                    week[day] = int(data)
                except ValueError:
                    raise ValueError(
                        'Day {day} data in entries {entries} is not a number'.format(day=day, entries=entries))
        elif spec == 'description':
            if description is not None:
                raise ValueError('Entries {entries} contain duplicate description field'.format(entries=entries))
            description = data
    if len(week) != 5:
        raise ValueError('Entries have missing days, only contains "{data}"'.format(data=", ".join(week.keys())))
    if description is None:
        raise ValueError('Entries {entries} does not contain a description'.format(entries=entries))
    return description, week


def generate_week_summary(description, week):
    week_value = []
    for day, value in week.items():
        day_value = {'day': day, 'value': value}
        if day in ('mon', 'tue', 'wed'):
            specific_value = day_value['square'] = value ** 2
        else:
            specific_value = day_value['double'] = value * 2
        day_value['description'] = '{description} {specific_value}'.format(description=description,
                                                                           specific_value=specific_value)

        week_value.append(day_value)
    return week_value


def process_csv_file(csv_file_path):
    entries = read_csv_file(csv_file_path)
    description, week = extract_week_information(entries)
    return generate_week_summary(description, week)


def main():
    for file_name, csv_file_path in get_csv_paths():
        print(file_name)
        pprint(process_csv_file(csv_file_path))


if __name__ == '__main__':
    main()
