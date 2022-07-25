from database import Database
from fastapi import FastAPI, Request
from handlers import get_geolocation
try:
    import boot    # the import itself will set the secret api keys in env
except Exception as e:
    print("you must set env variables for code to work, add a boot file")
    print(e)
    exit()

app = FastAPI()


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
    def post_timeslots(self, req: Request):
        params = req.query_params
        return {"Hello world!"}

    @app.post("/deliveries/{delivery_id}/complete")
    def post_deliveries(self, req: Request, delivery_id):
        return {"Hello world!"}

    @app.delete("/deliveries/{delivery_id}")
    def delete_delivery(self, req: Request, delivery_id):
        return None







