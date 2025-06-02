from datetime import date, time, datetime, timedelta
from dataclasses import dataclass, field
import json

import config
from enums import *

@dataclass
class Event:
    id: int
    name: str
    date: date
    time: time
    routes: list = field(default_factory=list)
    age_groups: list['AgeGroup'] = field(default_factory=list)
    riders: list['Rider'] = field(default_factory=list)
    marathon_start_time:datetime = None
    halfmarathon_start_time:datetime = None
    log: list = field(default_factory=list)

    def count_absolute_places(self):
        absolute: list[tuple[int, Rider]] = []

        for rider in self.riders:
            if rider.age_group != "Полумарафон" and rider.result_seconds:
                absolute.append((rider.result_seconds, rider))
        
        absolute.sort(key=lambda x: x[0])

        place = 0
        previous_seconds = None
        for seconds, rider in absolute:
            if seconds != previous_seconds:
                place += 1

            rider.absolute_place = place
            rider.absolute_score = config.RATING_SCORES.get(place, 0)

            previous_seconds = seconds
    

@dataclass
class Rider:
    number: int
    last_name: int
    first_name: int
    birthday: date
    gender: Gender
    phone_number: str
    distance: int
    age_group: 'AgeGroup' = None
    category: Category = Category.Default
    start_time: datetime = None
    lap_times: list[datetime] = field(default_factory=list)
    finish_time: datetime = None
    place: int = None
    absolute_place:int = None
    absolute_score:int = None
    user_profile_id: int = None
    started: bool = True
    dsq: bool = False
    dnf: bool = False
    helmet_not_needed: bool = True
    payment_confirmed: bool = True

    def format_surname_number(self):
        return f"{self.number or 999} {self.last_name}"

    def format_name(self):
        return f"{self.last_name} {self.first_name}"
    
    def format_birthday(self):
        return self.birthday.strftime("%d.%m.%Y")
    
    def age(self, date_:date=None):
        date_ = date_ or date.today()
        age = date_.year - self.birthday.year

        date_ = date_.replace(year=self.birthday.year)
        if date_ < self.birthday:
            age -= 1
        return age
    
    def set_age_group(self, event:Event):
        if self.category == Category.Elite:
            self.age_group = "Элита"

        elif self.category == Category.Junior:
            self.age_group = "Юниоры"

        elif self.distance == max(event.routes):
            for age_group in event.age_groups:
                if age_group.age_min <= self.age() <= age_group.age_max and self.gender == age_group.gender:
                    self.age_group = age_group
                    break

        else:
            self.age_group = "Полумарафон"
                
        return self.age_group

    def payment_confirmed_state_changed(self, state:bool):
        self.payment_confirmed = bool(state)

    def started_state_changed(self, state:bool):
        self.started = bool(state)

    def helmet_not_needed_state_changed(self, state:bool):
        self.helmet_not_needed = bool(state)

    def start(self):
        self.start_time = datetime.now()

    def finish(self):
        if len(self.lap_times) < (self.laps - 1):
            self.lap_times.append(datetime.now())
        else:
            self.finish_time = datetime.now()

    @property
    def laps(self):
        if self.age_group == "Полумарафон":
            return config.LAPS_HALFMARATHON
        else:
            return config.LAPS_MARATHON

    def cancel_finish(self):
        self.finish_time = None
        self.dsq = False
        self.dnf = False

    def did_not_finish(self):
        self.dnf = True

    def disqualify(self):
        self.dsq = True

    def render_result(self, lap:int=None):
        if self.dsq:
            return "DSQ"
        if self.dnf:
            return "DNF"
        if not self.started and self.start_time is not None:
            return "DNS"        
        if self.start_time is None:
            return ""
        
        if lap is None:
            if self.finish_time is not None:
                t = round(self.result.total_seconds())
            else:
                return ""
        elif lap < len(self.lap_times):
            t = round((self.lap_times[lap] - self.start_time).total_seconds())
        else:
            return ""
        
        h, t = divmod(t, 3600)
        m, s = divmod(t, 60)

        return F"{h:02d}:{m:02d}:{s:02d}"      

    @property
    def result(self):
        if self.start_time is None or self.finish_time is None:
            return None
        return  self.finish_time - self.start_time
    
    @property
    def result_seconds(self):
        if self.result is None:
            return None
        return round(self.result.total_seconds())
    
    @staticmethod
    def sort_key(rider:'Rider'):
        return (
            rider.result is None, 
            rider.dnf, 
            rider.dsq, 
            not rider.started,
            rider.result)


@dataclass(unsafe_hash=True)
class AgeGroup:
    birthday_min: date
    birthday_max: date
    age_min: int
    age_max: int
    gender: Gender

    def __str__(self):
        gender = ["М", "Ж"][self.gender == Gender.F]
        return f"{gender} {self.age_min}-{self.age_max}"

@dataclass
class Result:
    event: int
    route: int
    user_profile: int
    number: int
    time: timedelta = None
    status: ResultStatus = ResultStatus.OK

    @classmethod
    def from_event(cls, event:Event) -> list['Result']:
        route_ids = [7, 6] # FIX ME - hardcode

        results = []
        marathon = max(event.routes)
        for rider in event.riders:
            kwargs = {}
            kwargs['event'] = event.id
            kwargs['route'] = route_ids[rider.distance != marathon]
            kwargs['user_profile'] = rider.user_profile_id
            kwargs['number'] = rider.number
            if rider.started == False:
                continue
            elif rider.dnf:
                kwargs['status'] = ResultStatus.DNF
            elif rider.dsq:
                kwargs['status'] = ResultStatus.DSQ
                if rider.start_time and rider.finish_time:
                    kwargs['time'] = rider.finish_time - rider.start_time
            else:
                kwargs['status'] = ResultStatus.OK
                if rider.start_time and rider.finish_time:
                    kwargs['time'] = rider.finish_time - rider.start_time
            

            instance = cls(**kwargs)
            results.append(instance)

        return results
