import os
import requests
import csv
import json
from datetime import datetime
from bs4 import BeautifulSoup


# get the HTML document
def collect_data(date: str):
    response = requests.get(url='https://kino.vl.ru/films/seances/')
    if response.status_code != 200:
        raise KeyError('Response is not 200')
    with open(f'data_{date}.html', 'w') as file:
        file.write(response.text)


# separate the day of the week and delete extra whitespaces
def get_clear_text(text: str) -> tuple[str, str]:
    text = text.strip()
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    found_day = None
    for day in days_of_week:
        rubbish = str(day + ', ')
        if rubbish in text:
            text = text.removeprefix(rubbish)
            found_day = day
            break
    return text, found_day


# list of pairs film_name - theatre (possibly more than one theatre)
def name_to_theatre(elem: BeautifulSoup) -> list[tuple[str, str]]:
    result = []
    film_name = elem.get_text().strip()
    for theatre in elem.parent.find(class_='table-responsive__theatre-name').find_all('a'):
        result.append((film_name, theatre.get_text()))
    return result


# write the event to the dict
def write_event(curr_date: str, curr_time: str, events: dict, pairs: list) -> None:
    for [name, theatre] in pairs:
        events[curr_date][curr_time].append((name, theatre))


# parse films from the HTML document
def parse_data(date: str) -> tuple:
    # `date` means the real today's date; `curr_date` and `curr_time` are intended for currently parsing elements
    with open(f'data_{date}.html') as file:
        soup = BeautifulSoup(file, 'html.parser')

    events = {}
    dates_days_of_week = {}
    curr_date = ""

    trs = soup.find_all('tr')
    i = 0
    while i < len(trs):  # while-loop is chosen to be able to skip some elements from the inside
        tr = trs[i]
        for_date = tr.find(class_="films-seances__seance-date")
        for_time = tr.find(class_='time')
        if for_date:  # new date mark
            curr_date, day_of_week = get_clear_text(for_date.get_text())
            dates_days_of_week[curr_date] = day_of_week
            events[curr_date] = {}
        elif for_time:  # new time mark (they have one time tag for several films)
            curr_time, _ = get_clear_text(for_time.get_text())
            events[curr_date][curr_time] = []
            for_name = trs[i].find(class_='table-responsive__film-name')
            write_event(curr_date, curr_time, events, name_to_theatre(for_name))  # the same elem contains film name
            if 'rowspan' in for_time.attrs:
                for j in range(int(for_time['rowspan']) - 1):  # the next `rowspan` elems contain films for `curr_time`
                    i += 1
                    for_name = trs[i].find(class_='table-responsive__film-name')
                    write_event(curr_date, curr_time, events, name_to_theatre(for_name))
        i += 1

    return events, dates_days_of_week


def save_data(events: dict, days_of_week: dict, date: str) -> None:
    # create json
    with open(f'data_{date}.json', 'w') as file:
        json.dump(events, file, indent=4, ensure_ascii=False)

    # write headers
    with open(f'data_{date}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ('Дата', 'День недели', 'Время', 'Фильм', 'Кинотеатр')
        )

    # write contents
    with open(f'data_{date}.csv', 'a') as file:
        writer = csv.writer(file)
        for [f_date, times] in events.items():
            day_week = days_of_week[f_date]
            for [time, films] in times.items():
                for [name, theatre] in films:
                    writer.writerow(
                        (f_date, day_week, time, name, theatre)
                    )

    os.system(f'libreoffice --convert-to ods data_{date}.csv')  # convert to .ods
    os.system(f'libreoffice --convert-to xlsx data_{date}.csv')  # and .xlsx


def main():
    os.chdir('data')
    t_date = datetime.now().strftime('%d_%m_%Y')
    collect_data(t_date)
    events, days_of_week = parse_data(t_date)
    save_data(events, days_of_week, t_date)
    os.chdir('..')
    

def fetch_data():
    main()


if __name__ == '__main__':
    main()
