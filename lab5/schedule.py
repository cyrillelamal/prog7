import json
import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

URI = 'https://guide.herzen.spb.ru/static/schedule_view.php?id_group=14203&sem=2'


def load_html(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


class Day:
    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name.strip().lower()


class Moment:
    def __init__(self, hour: int, minute: int) -> None:
        self.hour = hour
        self.minute = minute

    def __hash__(self) -> int:
        return hash((self.hour << 1) + (self.minute << 2))

    def __str__(self) -> str:
        return f'{self.hour}:{self.minute}'


class ClassDuration:
    def __init__(self, start: Moment, end: Moment) -> None:
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'{self.start}-{self.end}'


class Row:
    def __init__(self, row: Tag) -> None:
        self.row = row

    @property
    def is_dayname(self) -> bool:
        return 0 < len(self.row.select('th.dayname'))

    @property
    def dayname(self) -> str:
        if self.is_dayname:
            return self.row.select('th.dayname')[0].text
        raise Exception('Row is not a dayname')

    @property
    def is_multiline(self) -> bool:
        for th in self.row.select('th'):
            if th.has_attr('rowspan'):
                return True
        return False

    @property
    def has_class_duration(self) -> bool:
        for th in self.row.select('th'):
            if ':' in th.text:
                return True
        return False

    @property
    def class_duration(self) -> ClassDuration:
        for th in self.row.select('th'):
            if ':' in th.text:
                matches = re.match(r'(?P<start>\d+:\d+).*?(?P<end>\d+:\d+)', th.text).groupdict()
                start = Moment(*matches['start'].split(':'))
                end = Moment(*matches['end'].split(':'))
                return ClassDuration(start, end)
        raise Exception('Row does not represent the class duration')

    @property
    def week_type(self) -> str:
        for th in self.row.select('th'):
            if ':' not in th.text:
                return th.text.strip()
        return ''

    @property
    def is_common(self) -> bool:
        for td in self.row.select('td'):
            if td.has_attr('colspan'):
                return True
        return False

    @property
    def classes(self) -> list:
        return [str(td) for td in self.row.select('td')]

    def __str__(self) -> str:
        return str(self.row)


def main(url: str):
    soup = BeautifulSoup(load_html(url), 'html.parser')

    tbody = soup.select('table.schedule > tbody')[0]  # type: Tag
    if tbody is None:
        raise Exception('No schedule container')

    schedule = dict()

    day = None
    class_duration = None

    previous = None

    for tr in tbody.select('tr'):  # type: Tag
        row = Row(tr)

        if row.is_dayname:
            day = Day(row.dayname)
            schedule[str(day)] = {}
            continue

        if row.has_class_duration:
            class_duration = row.class_duration

        if row.is_multiline:
            previous = row
            continue
        else:
            day = str(day)
            if day not in schedule:
                schedule[day] = {}

            class_duration = str(class_duration if previous is None else previous.class_duration)
            if class_duration not in schedule[day]:
                schedule[day][class_duration] = {}

            week_type = str(row.week_type)
            if week_type not in schedule[day][class_duration]:
                schedule[day][class_duration][week_type] = []  # TODO: fill with class objects

            # current (bottom)
            schedule[day][class_duration][week_type] = row.classes
            # previous (upper)
            if previous is not None:
                week_type = str(previous.week_type)
                if week_type not in schedule[day][class_duration]:
                    schedule[day][class_duration][week_type] = []
                schedule[day][class_duration][week_type] = previous.classes

            previous = None

    print(json.dumps(schedule))


if __name__ == '__main__':
    main(URI)
