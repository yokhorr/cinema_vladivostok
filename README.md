# Description
A [bot](https://t.me/cinema_vladivostok_bot) to get the current timetable of films in Vladivostok in simple table format (`.xlsx`, `.ods`, `.csv` or even `.json`).
With this format you can filter and sort the information about films as you wish.
You can filter theatres, sort events by date and time, exclude / include specified films, etc.
In a word, anything your table editor and your skills allow you to do.

# Usage
1. Clone this repository: `git clone https://github.com/yokhor/cinema_vladivostok.git`
2. Install required modules: `pip install -r requirements.txt`
3. Create a `.bot_token.txt` file and write _your bot_ token to it (you can get it with [BotFather](https://t.me/BotFather))
4. You need to have `libreoffice` installed. Otherwise, find a different way to convert files from `.csv` to `.ods` and `.xlsx`
   and write it in `fetch_data.py` -> `save_data()` in the end
5. Run `main.py` to start the bot

# Documentation
### `main.py`
The main script starting the bot is `main.py`. Every message sent to the bot is logged in `log.csv`.
Receiving the `/showtimes` command bot checks first whether a schedule of the current date already exists.
If not, it starts module `fetch_data.py` to get it.
With `/showtimes {ext}` (without a dot `.`) user can request a `.csv`, `.ods` or `.json` file (default is `.xlsx`).

### `fetch_data.py`
In module `fetch_data.py` function `collect_data` gets an HTML document from https://kino.vl.ru/films/seances/.
If the response code is not `200`, the module returns an error.

Then the received document is parsed in `parse_data` using `BeautifulSoup`. The data collected is film date, time, name and theatre.
Two films are considered as different events if all above parameters differ.

`parse_cost` additionally parses the cost of the ticket for the event.

Finally, events are written to a `.csv` and a `.json` files named with the date of the request in `save_data`.
The `.csv` file is converted to `.xlsx` and `.ods` with `libreoffice`.

### Other files
- `requirements.txt` contain required libraries
- `CHANGELOD.md` describes updates for every new version
- `greet.md` and `info.md` are for the bot `/start` and `/info` commands

# Libraries
- Python bot is written with `aiogram`.
- For parsing `BeautifulSoup` is used.
- Getting data from the resource is used with `requests` library.

# Plans
- [ ] Replace dictionary `events` with a list of tuples
- [ ] Add other cities from the same [source](https://kino.vl.ru/films/seances/)
- [ ] Find other data resources with better format to parse (hopefully `.json`)
- [ ] Scrap more info: genre, ~~cost~~, description, link, film length
- [ ] Filter received events right from the bot
- [ ] Write documentation in Russian
- [ ] Find another way to convert files from `.csv` to `.xlsx` and `.ods`

# Gallery
### Bot in Telegram
<img src="https://github.com/yokhor/cinema_vladivostok/assets/97782643/bbe3e540-9cde-41cc-b518-b48616bee020" alt="Bot in Telegram" width="100%"/>

### Table in LibreOffice
<img src="https://github.com/yokhor/cinema_vladivostok/assets/97782643/56282270-50a7-446f-97eb-5a820afb5a98" alt="Table in LibreOffice" width="100%"/>

### Filtering data in table
<img src="https://github.com/yokhor/cinema_vladivostok/assets/97782643/5a14bd39-ce3d-402d-9c84-96e6938e93e0" alt="Filtering data in table" width="100%"/>
