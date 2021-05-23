import datetime as dt

from O365 import Account, FileSystemTokenBackend

from cal import Calendar
from event import Event
from pytz import timezone

class CalendarFetcher:
    def __init__(self, token_file_name, tenant_id, creds):
        token_backend = FileSystemTokenBackend(token_path='.', token_filename=token_file_name)
        self.account = Account(creds, token_backend=token_backend, tenant_id=tenant_id)

    def fetch_calendar(self):
        self.account.con.refresh_token()
        schedule = self.account.schedule()

        calendar = schedule.get_default_calendar()

        now = dt.datetime.now(tz=timezone("Europe/London"))
        tomorrow = now + dt.timedelta(days=1)
        tomorrow.replace(hour=0, minute=0, second=0)
        q = calendar.new_query('start').greater_equal(now)
        q.chain('and').on_attribute('end').less_equal(tomorrow)

        events = map(lambda e: Event(e.start, e.end, e.subject, e.start.day != now.day), filter(lambda e: e.end > now, calendar.get_events(query=q, include_recurring=True)))

        sorted_events = sorted(events, key=lambda e: e.start)
        return Calendar(self.account.get_current_user().display_name, now, list(sorted_events))