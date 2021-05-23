import datetime
from dataclasses import dataclass


@dataclass
class Event:
    start: datetime.datetime
    end: datetime.datetime
    name: str
    different_day: bool

    def __hash__(self) -> int:
        return sum([hash(a) for i, a in enumerate([str(self.start.time()), str(self.end.time()), self.name, self.different_day])])

