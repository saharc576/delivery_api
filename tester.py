import time

import requests
from multiprocessing import Process
from database import db

def test_deliveries_daily():
    req = requests.get('http://0.0.0.0:8000/deliveries/daily/')
    print(req.json())


def test_deliveries_weekly():
    req = requests.get('http://0.0.0.0:8000/deliveries/weekly/')
    print(req)


def test_resolve_address():
    req = requests.post('http://0.0.0.0:8000/resolve-address/', json={"searchTerm": "Dizengoff, 63117 Tel Aviv-Yafo, Israel"}).json()
    print(req)


def test_post_timeslots():
    req = requests.post('http://0.0.0.0:8000/timeslots/',
                        json={"address": "Dizengoff, 63117 Tel Aviv-Yafo, Israel"}).json()
    print(req)


def test_post_deliveries(name):
    req = requests.post('http://0.0.0.0:8000/deliveries/',
                        json={"user": name, "timeslotId": "cff4eee495bee7582c3f629425edcb5db7c790f9"}).json()
    print(req)

def test_post_deliveries_complete():
    req = requests.post('http://0.0.0.0:8000/deliveries/2/complete',).json()
    print(req)


def test_delete_delivery():
    req = requests.delete('http://0.0.0.0:8000/deliveries/1/',
                          json={"searchTerm": "Dizengoff, 63117 Tel Aviv-Yafo, Israel"}).json()
    print(req)


def test_concurrent_post():
    p1 = Process(target=test_post_deliveries, args=("sahar",))
    p2 = Process(target=test_post_deliveries, args=("oren",))
    p1.start()
    p2.start()


if __name__ == "__main__":
    print("starting tests...")
    db.print_table("tables before tests:")
    time.sleep(0.3)
    test_concurrent_post()
    time.sleep(0.3)
    db.print_table("tables after concurrent post:")
    time.sleep(0.3)
    test_post_timeslots()
    time.sleep(0.3)
    test_deliveries_daily()
    time.sleep(0.3)
    test_post_deliveries(name="sahar")
    time.sleep(0.3)
    db.print_table("tables after post of sahar:")
    time.sleep(0.3)
    test_deliveries_daily()
    time.sleep(0.3)
    test_post_deliveries(name="oren")
    time.sleep(0.3)
    db.print_table("tables after post of oren:")
    time.sleep(0.3)
    test_delete_delivery()
    time.sleep(0.3)
    db.print_table("tables after deletion of id 1:")
    time.sleep(0.3)
    test_post_deliveries_complete()
    time.sleep(0.3)
    db.print_table("tables after completion of id 2:")
