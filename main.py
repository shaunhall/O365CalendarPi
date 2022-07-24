import argparse
import logging
import os

import display
from cal_fetcher import CalendarFetcher
from creds import credentials

parser = argparse.ArgumentParser(description='Render your O365 calendar on a pi')
parser.add_argument('--rotate', default=False,
                    help='rotate the display by 180 degrees')
args = parser.parse_args()

state_path = "./state_hash.txt"
def is_new_state(state):
    if os.path.exists(state_path):
        with open(state_path) as f:
            return f.readline() != state
    else:
        return True

def write_state(state):
    with open(state_path, "w") as f:
        f.write(state)


fetcher = CalendarFetcher("o365_token.txt", "233b013b-d83e-4f7a-86ff-f2e4e7e6946b", credentials)
calendar = fetcher.fetch_calendar()
state = str(hash(calendar))
if is_new_state(state):
    write_state(state)
    display.render(calendar, rotate=args.rotate)
else:
    logging.info("No change to calendar")
# from event import Event
#
# display.render(Calendar("Shaun Hall", datetime.datetime.now(),
#                         [Event(datetime.datetime.now(), datetime.datetime.now(), "Event number 1"),
#                          Event(datetime.datetime.now() + datetime.timedelta(hours=1),
#                                datetime.datetime.now() + datetime.timedelta(hours=2), "Event number 2"),
#                          Event(datetime.datetime.now() + datetime.timedelta(hours=2),
#                                datetime.datetime.now() + datetime.timedelta(hours=5), "Event number 3")
#                          ]))
