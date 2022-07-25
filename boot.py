import os
import handlers
from database import Database

os.environ["HOLIDAY_KEY"] = "YOUR API KEY"
os.environ["GEO_KEY"] = "YOUR API KEY"
db = Database()
timeslots = handlers.get_valid_time_slots()
db = Database()
db.insert_time_slots(timeslots)
print(db.get_all_timeslots())
print("booted")
