import requests


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


def test_post_deliveries(name="sahar"):
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


if __name__ == "__main__":
    # test_post_timeslots()
    test_deliveries_daily()
    test_post_deliveries()
    test_deliveries_daily()
    test_post_deliveries(name="oren")
    # test_delete_delivery()
    test_post_deliveries_complete()