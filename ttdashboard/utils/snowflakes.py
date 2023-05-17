import string
import datetime
import os
from typing import Counter

import map

epoch = datetime.datetime(year=2021, month=1, day=1)


def complete_bin(number, length):
    """
    Complete a bin with zeros.
    """
    return bin(number)[2:].zfill(length)

def snowflake(object, original_id) -> int:
    """
    Generate a snowflake.
    """
    types = {
        "<class 'map.models.Player'>": 1,
        "<class 'map.models.Tank'>": 2,
        "<class 'map.models.Game'>": 3,
        "<class 'map.models.BaseEvent'>": 4,
        "<class 'map.models.MoveEvent'>": 5,
        "<class 'map.models.ShootEvent'>": 5,
        "<class 'map.models.TransferEvent'>": 6,
        "<class 'map.models.RangeUpgradeEvent'>": 7,
        "<class 'map.models.VoteEvent'>": 8
    }
    if "counter" not in globals():
        global counter
        counter = 0
    counter += 1
    original_id = complete_bin(counter, 10)
    object_type = types[str(type(object))]
    timestamp = complete_bin((datetime.datetime.utcnow() - epoch).seconds, 25)
    pid = complete_bin(os.getpid(), 5)
    return object_type + int(timestamp + pid + original_id, 2)
