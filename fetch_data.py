import requests
from bs4 import BeautifulSoup
import csv
import json
from datetime import datetime


# get the HTML document
def collect_data(date: str):
    response = requests.get(url='https://kino.vl.ru/films/seances/')
    with open(f'info_{date}.html', 'w') as file:
        file.write(response.text)


# delete day of the week and extra whitespaces
def get_clear_text(text: str):
    result = ""
    prev = ''
    skip = True
    for c in text:
        if skip and not c.isdigit():
            continue
        if c == prev == ' ':
            break
        skip = False
        result += c
        prev = c
    return result[:-1]
        
        
# write the event; if success, return true
def write_event(curr_date, curr_time, curr_name, theatres, events):
    if curr_date and curr_time and curr_name:  # protection from first lines rubbish
        for theatre in theatres:  # several theatres for the same film at the same time
            events[curr_date][curr_time].append((curr_name, theatre))
        return True
    return False


# parse films from the HTML document
def parse_data(date: str):
    # `date` means the real today's date; `curr_date` and `curr_time` are intended for currently parsing elements
    with open(f'info_{date}.html') as file:
        soup = BeautifulSoup(file, 'html.parser')

    events = {}
    curr_date = ""
    curr_time = ""
    curr_name = ""
    curr_theatres = []
    for tr in soup.find_all('tr'):
        tds = tr.contents
        for td in tds:
            try:
                if td.contents[1]['class'][0] == 'films-seances__seance-date':  # found new date mark
                    if write_event(curr_date, curr_time, curr_name, curr_theatres, events):
                        curr_theatres = []
                    curr_date = get_clear_text(td.contents[1].get_text()[1:])
                    events[curr_date] = {}
                    curr_time = ""
            except:
                try:
                    if curr_time and td['class'][0] == 'table-responsive__theatre-name':  # found a new theatre name
                        theatres = td.get_text()[1:-1]
                        tmp = theatres.split('\n')  # one film at the same time can have several theatres
                        for e in tmp:
                            curr_theatres.append(e)
                    else:
                        if write_event(curr_date, curr_time, curr_name, curr_theatres, events):
                            curr_theatres = []
                        if td['class'][0] == 'time':  # found a new time mark (they have one tag for several films)
                            curr_time = get_clear_text(td.get_text())
                            events[curr_date][curr_time] = []
                        elif curr_time and td['class'][0] == 'table-responsive__film-name':  # found a new film name
                            curr_name = td.get_text()[1:-1]
                except:
                    continue
    return events


def save_data(events: dict, date: str):
    # create json

    # with open(f'info_{date}.json', 'w') as file:
    #     json.dump(events, file, indent=4, ensure_ascii=False)

    with open(f'data_{date}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            ('Date', 'Time', 'Film', 'Theatre')
        )

    with open(f'data_{date}.csv', 'a') as file:
        writer = csv.writer(file)
        for [f_date, times] in events.items():
            for [time, films] in times.items():
                for [name, theatre] in films:
                    writer.writerow(
                        (f_date, time, name, theatre)
                    )
    

def main():
    t_date = datetime.now().strftime('%d_%m_%Y')
    collect_data(t_date)
    events = parse_data(t_date)
    save_data(events, t_date)
    

def fetch_data():
    main()


if __name__ == '__main__':
    main()
