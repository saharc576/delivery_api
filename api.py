import os
import requests
from requests.structures import CaseInsensitiveDict
import urllib.parse
from database import Database
from fastapi import FastAPI, Request
import boot     # the import itself will set the secret api keys in env

app = FastAPI()
exit()


class Api:

    def __init__(self):
        self.db = Database()

    @app.get("/deliveries/daily")
    def deliveries_daily(self):
        return {"Hello world!"}

    @app.get("/deliveries/weekly")
    def deliveries_weekly(self):
        return {"Hello world!"}

    @app.post("/resolve-address")
    def post_resolve_address(self, req: Request):
        params = req.query_params
        res = get_geolocation(params)
        return {res}

    @app.post("/timeslots")
    def post_resolve_address(self, req: Request):
        params = req.query_params
        return {"Hello world!"}

    @app.post("/deliveries/{delivery_id}/complete")
    def post_resolve_address(self, req: Request, delivery_id):
        return {"Hello world!"}

    @app.delete("/deliveries/{delivery_id}")
    def delete_delivery(self, req: Request, delivery_id):
        return None


def get_geolocation(text):
    t = urllib.parse.quote(text)
    url = f"https://api.geoapify.com/v1/geocode/search?text={t}&apiKey={os.getenv('GEO_KEY')}"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)

    return resp.text

def get_holidays():
    url = f"https://holidayapi.com/v1/holidays?country=IL&year=2021&pretty&key={os.getenv('HOLIDAY_KEY')}"
    payload = f'country=IL&year=2021&pretty=&key={os.getenv("HOLIDAY_KEY")}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text





