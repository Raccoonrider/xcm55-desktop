import os
import json
from urllib.request import Request, urlopen, HTTPError

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

import config
from api.serializers import *
from models import Event, Rider, AgeGroup, Result

headers = {
    "Authorization": f'Token {os.environ["AUTH_TOKEN"]}',
    "User-Agent": "XCM55-desktop",
    "Content-Type": "application/json",
}

def load_event() -> Event:
    url = f"https://xcm55.ru/api/events/{config.EVENT_ID}/"
    request = Request(url, headers=headers)
    response = urlopen(request, timeout=30)
    data = json.load(response)
    object = EventSerializer().deserialize(data)
    return object


def load_riders() -> list[Rider]:
    url = f"https://xcm55.ru/api/events/{config.EVENT_ID}/applications/"
    request = Request(url, headers=headers)
    response = urlopen(request, timeout=30)
    data = json.load(response)
    objects = [RiderSerializer().deserialize(x) for x in data]
    return objects


def load_age_groups() -> list[AgeGroup]:
    url = f"https://xcm55.ru/api/events/{config.EVENT_ID}/age_groups/"
    request = Request(url, headers=headers)
    response = urlopen(request, timeout=30)
    data = json.load(response)
    objects = [AgeGroupSerializer().deserialize(x) for x in data]
    return objects

def post_results(results:list[Result]):
    url = f"https://xcm55.ru/api/events/results/add/"
    serializer = ResultSerializer()

    data = json.dumps([serializer.serialize(result) for result in results])
    try:
        request = Request(url, data=data.encode('utf-8'), headers=headers)
        print(request.data)
        response = urlopen(request, timeout=30)
    except HTTPError as e:
        print(e.read().decode('utf-8'))


if __name__ == '__main__':
    riders = load_riders()
    for x in riders:
        print(x)

    age_groups = load_age_groups()
    for x in age_groups:
        print(x)

    print(load_event())