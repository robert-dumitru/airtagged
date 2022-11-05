import os
import json
from ..classes import Location

def airtag_location(name: str) -> Location:
    path = os.environ["HOME"] + "/Library/Caches/com.apple.findmy.fmipcore/Items.data"
    with open(path) as f:
        data = json.loads(f.read())
        f.close()
    data = data[name]
    return Location(
        data["longitude"],
        data["latitude"],
        None,
        data["timestamp"]
    )

