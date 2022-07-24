import sqlite3
import datetime


class Database:
    def __init__(self):
        self.con = sqlite3.connect('deliveries.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE deliveries
                                  (delivery_id text, username text, start_time timestamp, end_time timestamp, complete int)''')

    def insert_to_table(self, delivery_id, username, start, end, complete=0):
        row = [delivery_id, username, start, end, complete]
        self.cur.execute("insert into deliveries values (?, ?, ?, ?, ?)", row)
        self.print_table("after insert")

    def set_complete(self, delivery_id_):
        self.cur.execute("UPDATE deliveries SET complete = 1 WHERE delivery_id = (?)", [delivery_id_])
        self.print_table(f"after set complete of delivery_id={delivery_id_}")

    def get_today_deliveries(self):
        self.cur.execute("SELECT * from deliveries WHERE start > (?)", [datetime.datetime.today().timestamp()])

    def get_week_deliveries(self):
        self.cur.execute("SELECT * from deliveries WHERE start > (?)", [datetime.datetime.today().timestamp()])

    def print_table(self, msg=""):
        print(msg)
        self.cur.execute("select * from deliveries ")
        print(self.cur.fetchall())
