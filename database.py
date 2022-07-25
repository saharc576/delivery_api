import json
import sqlite3
import datetime
import os
from handlers import get_geolocation


class Database:
    def __init__(self):
        self.counter = 0
        self.con = sqlite3.connect('deliveries_data.db', check_same_thread=False)
        self.cur = self.con.cursor()
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = self.cur.fetchall()
        if ("deliveries",) not in table_names:
            self.cur.execute('''CREATE TABLE deliveries
                                      (id int,
                                      username text, 
                                      timeslot_id text, 
                                      complete int)''')
        if ("timeslots",) not in table_names:
            self.cur.execute('''CREATE TABLE timeslots
                                              (start_time timestamp, 
                                              end_time timestamp, 
                                              timeslot_id text,
                                              addresses text,
                                              taken int)''')

    def insert_delivery_to_table(self, username, timeslot_id, complete=0):
        self.cur.execute("SELECT taken from timeslots WHERE timeslot_id = ?", (timeslot_id,))
        taken = self.cur.fetchone()
        if taken[0] < 2:
            self.counter += 1
            row = [self.counter, username, timeslot_id, complete]
            self.cur.execute("insert into deliveries values (?, ?, ?, ?)", row)
            self.cur.execute("UPDATE timeslots SET taken = ? WHERE timeslot_id = ?", (taken[0] + 1, timeslot_id))
            self.print_table("after insert")
            return self.counter
        print(f"timeslot {timeslot_id} is taken by two deliveries already")
        return False

    def init_time_slots(self, timeslots):
        if not os.getenv("INIT_TIMESLOTS"):
            for timeslot in timeslots:
                start = datetime.datetime.strptime(timeslot["start"], "%d/%m/%y %H:%M").timestamp()
                end = datetime.datetime.strptime(timeslot["end"], "%d/%m/%y %H:%M").timestamp()
                row = [start, end, timeslot["id"], json.dumps(get_geolocation(timeslot["address"])), 0]
                self.cur.execute("insert into timeslots values (?, ?, ?, ?, ?)", row)
            os.environ["INIT_TIMESLOTS"] = "TRUE"

    def get_all_timeslots(self):
        self.cur.execute("SELECT * from timeslots WHERE taken < 2")
        return self.cur.fetchall()

    def set_complete(self, delivery_id):
        self.cur.execute("UPDATE deliveries SET complete = 1 WHERE id = ?", (delivery_id,))
        self.print_table(f"after set complete of delivery_id={delivery_id}")

    def get_today_deliveries(self):
        self.cur.execute("SELECT timeslot_id from deliveries")
        delivery_timeslots = self.cur.fetchall()
        self.cur.execute("SELECT timeslot_id from timeslots WHERE start_time >= ?", (datetime.datetime.today().timestamp(),))
        timeslots = self.cur.fetchall()
        return list(set(delivery_timeslots).intersection(set(timeslots)))

    def get_week_deliveries(self):
        return self.get_today_deliveries()

    def delete_delivery(self, delivery_id):
        self.cur.execute("Delete from deliveries Where id = ?", (delivery_id,))
        deliveries = self.cur.fetchall()
        for d in deliveries:
            freed_timeslot_id = d[1]
            self.cur.execute("SELECT taken from timeslots WHERE timeslot_id = ?", (freed_timeslot_id,))
            taken = self.cur.fetchone()
            self.cur.execute("UPDATE timeslots SET taken = ? WHERE id = ?", (taken[0] - 1, freed_timeslot_id))



    def print_table(self, msg=""):
        print(msg)
        self.cur.execute("select * from deliveries ")
        print(self.cur.fetchall())


db = Database()
