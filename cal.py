import datetime
from dataclasses import dataclass
from typing import List

from event import Event


@dataclass
class Calendar:
    name: str
    last_updated: datetime.datetime
    events: List[Event]

    def __hash__(self) -> int:
        return hash(str(self.last_updated.day)) + (0 if not self.events else sum(hash(e)**i for i, e in enumerate(self.events)))

