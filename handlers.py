import datetime
import hashlib
import os
import requests
from requests.structures import CaseInsensitiveDict
import urllib.parse
import json


def get_geolocation(text):
    t = urllib.parse.quote(text)
    url = f"https://api.geoapify.com/v1/geocode/search?text={t}&apiKey={os.getenv('GEO_KEY')}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers).text
    lat = json.loads(resp)["features"][0]["properties"]["lat"]
    lon = json.loads(resp)["features"][0]["properties"]["lon"]
    return f"{lat}|{lon}"


def reverse_geolocation(lat, lon):
    lat = float(lat.replace('"', ""))
    lon = float(lon.replace('"', ""))
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={float(lat)}&lon={lon}&format=json&apiKey={os.getenv('GEO_KEY')}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers).text
    address = json.loads(resp)["results"][0]["formatted"]
    return address


def get_holidays():
    url = f"https://holidayapi.com/v1/holidays?country=IL&year=2021&pretty&key={os.getenv('HOLIDAY_KEY')}"
    payload = f'country=IL&year=2021&pretty=&key={os.getenv("HOLIDAY_KEY")}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


def get_valid_time_slots(path_to_static_json="timeslots.json"):
    valid = []
    f = open(path_to_static_json, "r")
    timeslots = json.load(f)["timeslots"]
    f.close()
    holidays = json.loads(get_holidays()) or {"holidays": []}
    for timeslot in timeslots:
        timeslot_date = datetime.datetime.strptime(timeslot["start"], "%d/%m/%y %H:%M")
        valid_timeslot = True
        for holiday in holidays["holidays"]:
            holiday_date = datetime.datetime.strptime(holiday["date"], "%Y-%m-%d")
            if holiday_date.date() == timeslot_date.date():
                valid_timeslot = False
                break
        if valid_timeslot:
            # if timeslot is good, add a unique id
            timeslot_id = hashlib.sha1(json.dumps(timeslot).encode()).hexdigest()
            timeslot["id"] = timeslot_id
            valid.append(timeslot)
        else:
            print(f"removed timeslot due to holiday collision {timeslot}")
    return valid
