import re
import json
import logging
import datetime
from dataclasses import dataclass, field, asdict

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from enums import *
from models import Event, Rider, AgeGroup, Result
from common.duration import duration_string


class BaseSerializer:
    def __init__(self, *args, **kwargs):
        # Keep this method to accept kwargs just in case
        pass

    model = None
    fields:list[str] = None
    fieldmap:dict = {}
    extra_fields:dict = {}

    currency_pattern = re.compile(r"^\d+\.\d\d$")
    date_pattern = re.compile(r"^\d\d\d\d\-\d\d\-\d\d$")
    time_pattern = re.compile(r"^\d\d\:\d\d\:\d\d$")
    datetime_pattern = re.compile(r"^\d\d\d\d\-\d\d\-\d\d.\d\d:\d\d:\d\d(?:\.\d+)")
    timedelta_pattern = re.compile(r"(\-?)P(\d*)DT(\d\d)H(\d\d)M(\d\d\.?\d*)S")

    def dumps(self, data) -> str:
        return json.dumps(data)
    
    def loads(self, data) -> dict:
        return json.loads(data)
    
    def try_serialize(self, *args, **kwargs) -> dict:
        try:
            return self.serialize(*args, **kwargs)
        except Exception:
            logging.exception(f"Failed to serialize an instance of {self.__class__.__name__}")
    
    def try_deserialize(self, *args, **kwargs):
        try:
            return self.deserialize(*args, **kwargs)
        except Exception:
            logging.exception(f"Failed to DEserialize an instance of {self.__class__.__name__}")

    def serialize(self, instance) -> dict:
        data = {}
        for field in self.fields:
            value = getattr(instance, field)
            data[self.fieldmap.get(field) or field] = self.dump_value(value)
        return data
    
    def deserialize(self, data:dict):
        kwargs = {}
        for field in self.fields:
            value = data.get(self.fieldmap.get(field) or field)
            value = self.load_value(value)
            kwargs[field] = value
        return self.model(**kwargs)
    
    def dump_value(self, value):
        if isinstance(value, datetime.datetime):
            return value.isoformat().replace('+00:00', '+03:00')
        
        elif isinstance(value, datetime.date):
            return value.isoformat()
        
        elif isinstance(value, datetime.time):
            return value.isoformat()
        
        elif isinstance(value, datetime.timedelta):
            if value < datetime.timedelta(0):
                sign = "-"
                value *= -1
            else:
                sign = ""

            days = value.days
            seconds = value.seconds
            microseconds = value.microseconds

            minutes = seconds // 60
            seconds %= 60

            hours = minutes // 60
            minutes %= 60

            ms = ".{:06d}".format(microseconds) if microseconds else ""
            return "{}P{}DT{:02d}H{:02d}M{:02d}{}S".format(
                sign, days, hours, minutes, seconds, ms
            )
        
        else:
            return value
        

    def load_value(self, value):
        if isinstance(value, str):        
            if s:=self.time_pattern.match(value):
                return datetime.time.fromisoformat(s.group(0))
            
            if s:=self.date_pattern.match(value):
                return datetime.date.fromisoformat(s.group(0))
            
            if s:=self.datetime_pattern.match(value):
                return datetime.datetime.fromisoformat(s.group(0))
            
            if m:=self.timedelta_pattern.match(value):
                sign = [1, -1][m.group(1) == '-']
                days = int(m.group(2))
                hours = int(m.group(3))
                minutes = int(m.group(4))
                seconds = float(m.group(5))
                return sign * datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

        return value

class RiderSerializer(BaseSerializer):
    model = Rider
    fields = [
        "number",
        "last_name",
        "first_name",
        "birthday",
        "gender",
        "phone_number",
        "category",
        "distance",
        "user_profile_id",
        "helmet_not_needed",
        "payment_confirmed",
    ]

    def deserialize(self, data: dict) -> Rider:
        instance = super().deserialize(data)
        instance: Rider
        instance.last_name = data['user_profile']['last_name']
        instance.first_name = data['user_profile']['first_name']
        instance.phone_number = data['user_profile']['phone_number']
        instance.birthday = datetime.date.fromisoformat(data['user_profile']['birthday'])
        instance.gender = Gender(data['user_profile']['gender'])
        instance.user_profile_id = data['user_profile']['id']
        instance.started = False

        return instance
    

class AgeGroupSerializer(BaseSerializer):
    model = AgeGroup
    fields = [
        'birthday_min',
        'birthday_max',
        'age_min',
        'age_max',
        'gender',
    ]

    def deserialize(self, data: dict) -> AgeGroup:
        return super().deserialize(data)


class EventSerializer(BaseSerializer):
    model = Event
    fields = [
        'id',
        'name',
        'date',
        'time',
    ]
    def deserialize(self, data: dict) -> Event:
        event = super().deserialize(data)
        event.routes = [x['distance'] for x in data['routes']]

        return event

class ResultSerializer:
    model = Result

    def serialize(self, instance:Result) -> dict:
        data = asdict(instance)
        if data.get('time'):
            data['time'] = duration_string(data.get('time'))
        data['status'] = int(data.get('status'))

        return data