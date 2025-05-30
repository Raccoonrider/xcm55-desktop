import pickle
import json
import logging

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

import config
from api.signal_router import router
from api.requests import load_event, load_age_groups, load_riders, post_results
from models import Result

def save_cache():
    if config.paths.cache.exists():
        config.paths.cache_backup.unlink(missing_ok=True)
        config.paths.cache.rename(config.paths.cache_backup)

    with open(config.paths.cache, mode="wb") as file:
        pickle.dump(event, file)

def load_cache():
    if config.paths.cache.exists():
        try:
            with open(config.paths.cache, mode="rb") as file:
                return pickle.load(file)
        except Exception:
            logging.exception("Could not load event from cache, retryingfrom backup...")
            if config.paths.cache_backup.exists():
                try:
                    with open(config.paths.cache_backup, mode="rb") as file:
                        return pickle.load(file)
                except Exception:
                    logging.exception("Could not load event from backup...")
            else:
                logging.error("Backup not found.")

def save_json():
    protocol = [
        {
            'number': x.number,
            'last_name': x.last_name,
            'first_name': x.first_name,
            'gender': x.gender,
            'user_profile_id': x.user_profile_id,
            'age_group': str(x.age_group),
            'start_time': x.start_time.isoformat() if x.start_time else None,
            'finish_time': x.finish_time.isoformat() if x.finish_time else None,
            'place': x.place,
            'started': x.started,
            'dsq': x.dsq,
            'dnf': x.dnf,

        }
        for x in event.riders
    ]

    if config.paths.protocol.exists():
        config.paths.protocol_backup.unlink(missing_ok=True)
        config.paths.protocol.rename(config.paths.protocol_backup)

    with open(config.paths.protocol, mode="wt", encoding='utf-8') as file:
        json.dump(protocol, file, ensure_ascii=False)


event = load_cache()

if event is None:
    event = load_event()
    event.age_groups = load_age_groups()
    event.riders = sorted(load_riders(), key=lambda x: (x.number or 0, x.last_name))
    event.log = []

    for rider in event.riders: 
        rider.set_age_group(event=event)

    save_cache()

def send_results():
    results = Result.from_event(event)
    post_results(results)