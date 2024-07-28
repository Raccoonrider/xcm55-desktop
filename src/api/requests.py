import json
from urllib.request import urlopen

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

import config
from api.serializers import RiderSerializer, AgeGroupSerializer, EventSerializer
from models import Event, Rider, AgeGroup

def load_event() -> Event:
    url = f"https://xcm55.ru/api/events/{config.EVENT_ID}/"
    response = urlopen(url, timeout=30)
    data = json.load(response)
    object = EventSerializer().deserialize(data)
    return object


def load_riders() -> list[Rider]:
    url = f"https://xcm55.ru/api/events/{config.EVENT_ID}/applications/"
    response = urlopen(url, timeout=30)
    data = json.load(response)
    objects = [RiderSerializer().deserialize(x) for x in data]
    return objects


def load_age_groups() -> list[AgeGroup]:
    url = f"https://xcm55.ru/api/events/{config.EVENT_ID}/age_groups/"
    response = urlopen(url, timeout=30)
    data = json.load(response)
    objects = [AgeGroupSerializer().deserialize(x) for x in data]
    return objects



if __name__ == '__main__':
    riders = load_riders()
    for x in riders:
        print(x)

    age_groups = load_age_groups()
    for x in age_groups:
        print(x)

    print(load_event())