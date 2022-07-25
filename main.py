import json

import uvicorn

from database import db
from fastapi import FastAPI, Request
from handlers import get_geolocation, reverse_geolocation
from pydantic import BaseModel
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
import boot    # the import itself will set the secret api keys in env

app = FastAPI()
router = InferringRouter()


# ========== Post requests bodies
class ResolveAddressData(BaseModel):
    searchTerm: str


class TimeSlotsData(BaseModel):
    address: str


class DeliveriesData(BaseModel):
    user: str
    timeslotId: str
# =================================


@cbv(router)
class Api:

    def __init__(self):
        self.db = db

    @router.get("/deliveries/daily")
    def deliveries_daily(self):
        response = self.db.get_today_deliveries()
        return {"daily": response}

    @router.get("/deliveries/weekly")
    def deliveries_weekly(self):
        response = self.db.get_week_deliveries()
        return {"weekly": response}

    @router.post("/resolve-address/")
    def post_resolve_address(self, data: ResolveAddressData):
        return data

    @router.post("/timeslots")
    def post_timeslots(self, data: TimeSlotsData):
        response = []
        address = data.address
        timeslots = self.db.get_all_timeslots()
        for timeslot in timeslots:
            lat, lon = timeslot[3].split("|")
            if address == reverse_geolocation(lat, lon):
                response.append(timeslot)
        return {"timeslots": response}

    @router.post("/deliveries/")
    def post_deliveries(self, data: DeliveriesData):
        user = data.user
        timeslot_id = data.timeslotId

        delivery_id = self.db.insert_delivery_to_table(username=user, timeslot_id=timeslot_id)
        if delivery_id:
            return {f"You booked a delivery with id {delivery_id}"}
        return {"Failed to book this timeslot"}

    @router.post("/deliveries/{delivery_id}/complete")
    def post_deliveries_complete(self, delivery_id):
        self.db.set_complete(delivery_id=delivery_id)
        return {f"Delivery {delivery_id} has set as complete!"}

    @router.delete("/deliveries/{delivery_id}")
    def delete_delivery(self, delivery_id):
        self.db.delete_delivery(delivery_id)
        return {f"Delivery {delivery_id} has been canceled!"}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)





