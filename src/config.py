from datetime import datetime
from pathlib import Path

EVENT_ID = 2

__location__ = Path.cwd()


class paths:
    localdata = __location__ / 'localdata'
    cache = localdata / 'event.pickle'
    protocol = localdata / 'protocol.json'
    
    backup = localdata / 'backup' 
    cache_backup = backup / 'event.pickle'
    protocol_backup = backup / 'protocol.json'



paths.localdata.mkdir(parents=True, exist_ok=True)
paths.backup.mkdir(parents=True, exist_ok=True)