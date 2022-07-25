import os
import handlers
from database import db

os.environ["HOLIDAY_KEY"] = "YOUR API KEY"
os.environ["GEO_KEY"] = "YOUR API KEY"
timeslots = handlers.get_valid_time_slots()
db.init_time_slots(timeslots)
print(f"testing insertion of timeslots:\n{db.get_all_timeslots()}")
print("booted")
