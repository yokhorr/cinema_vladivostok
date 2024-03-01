# Version 1.4 (02.03.24):
- added 10 other cities
- added `cities.txt`

# Version 1.3 (01.03.24):
- added ticket cost
  - added function `parse_cost`
- now script works a couple of minutes, so the first requested takes a long time

# Version 1.2 (29.02.24):
- added `requrements.txt`
- added some annotations
- changed `.gitignore`
- added `data` directory for all documents
- fixed pathways
- added log file creation if not one
- information about available formats moved from `greet.md` to `info.md`
- written a detailed `README.md`


# Version 1.1 (28.02.24):
- completely rewritten function `parse_data`:
  - removed try-except constructions
    - `<tr>` tags now checked by classes they contain (or not)
    - when found time mark all films at this time are added to dict
      - changed way of handling multiple theatres for the same film 
- added annotations
- added days of the week
- added `CHANGELOD.md`
- added logging
- updated Telegram bot:
  - added `/info` command
  - added commands menu
  - added description
  - added choice of file format (`.csv` `.ods`, `.xlsx`)
- added conversion from `.csv` to ``.ods`` and `.xlsx`
- added `greet.md`


# Version 1.0 (27.02.24)
- the minimum viable product created