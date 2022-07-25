import os
import handlers
from database import db

os.environ["HOLIDAY_KEY"] = "7ad297dc-a37e-4129-8a00-20107f4960ee"
os.environ["GEO_KEY"] = "d278b6c8518f4dbfbe9d5942f2c40ff2"
timeslots = handlers.get_valid_time_slots()
db.init_time_slots(timeslots)
print(f"testing insertion of timeslots:\n{db.get_all_timeslots()}")
print("booted")
