import json
import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


def load_html(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def is_button(tag: Tag) -> bool:
    if tag is None or tag.name is None:
        return False

    return 'button' == tag.name.strip().lower()


def parse_schedule_list(url: str) -> dict:
    soup = BeautifulSoup(load_html(url), 'html.parser')

    schedule = dict()

    institutes = soup.select('td.body > div > h3')
    group_containers = soup.select('td.body > div > div')

    for institute, group_container in zip(institutes, group_containers):
        institute_name = institute.select_one('a').text.strip()
        schedule[institute_name] = dict()

        forms = group_container.select('h4')
        group_lists = group_container.select('ul')

        for form, group_list in zip(forms, group_lists):
            form_name = form.text
            schedule[institute_name][form_name] = dict()

            for group in group_list.select('li'):
                group_name = group.contents[0].text.strip()
                schedule[institute_name][form_name][group_name] = dict()

                buttons = filter(is_button, group.contents[1])
                for button in buttons:  # type: Tag
                    if button.has_attr('onclick'):
                        fn = button.attrs.get('onclick')
                        matches = re.search(r'open\(\'(?P<path>.*?)\'', fn)
                        if matches:
                            schedule_name = button.text.strip()
                            path = matches.group('path').strip()
                            link = f'https://guide.herzen.spb.ru{path}'
                            schedule[institute_name][form_name][group_name][schedule_name] = link

    return schedule


def main(url: str) -> None:
    schedule = parse_schedule_list(url)
    print(json.dumps(schedule))
    exit(0)


if __name__ == '__main__':
    main('https://guide.herzen.spb.ru/static/schedule.php')
