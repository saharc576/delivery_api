import json
import signal
import time
from multiprocessing import Queue
from threading import Thread

import uvicorn
from database import db
from fastapi import FastAPI
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


consumer: Thread
buffer = Queue()


@cbv(router)
class Api:

    @router.get("/deliveries/daily")
    def deliveries_daily(self):
        response = db.get_today_deliveries()
        return {"daily": response}

    @router.get("/deliveries/weekly")
    def deliveries_weekly(self):
        response = db.get_week_deliveries()
        return {"weekly": response}

    @router.post("/resolve-address/")
    def post_resolve_address(self, data: ResolveAddressData):
        return data

    @router.post("/timeslots")
    def post_timeslots(self, data: TimeSlotsData):
        response = []
        address = data.address
        timeslots = db.get_all_timeslots()
        for timeslot in timeslots:
            lat, lon = timeslot[3].split("|")
            if address == reverse_geolocation(lat, lon):
                response.append(timeslot)
        return {"timeslots": response}

    @router.post("/deliveries/")
    def post_deliveries(self, data: DeliveriesData):
        global buffer
        user = data.user
        timeslot_id = data.timeslotId
        delivery_id = db.get_and_increase_counter()
        buffer.put((user, timeslot_id))
        return {f"We are booking a delivery with id {delivery_id} for you!"}

    @router.post("/deliveries/{delivery_id}/complete")
    def post_deliveries_complete(self, delivery_id):
        db.set_complete(delivery_id=delivery_id)
        return {f"Delivery {delivery_id} has set as complete!"}

    @router.delete("/deliveries/{delivery_id}")
    def delete_delivery(self, delivery_id):
        db.delete_delivery(delivery_id)
        return {f"Delivery {delivery_id} has been canceled!"}


def queue_consumer():
    global buffer
    print(f"queue_consumer started....")
    while True:
        # retrieve an item
        item = buffer.get()
        if not item:
            time.sleep(0.2)
            continue
        user, timeslot_id = item
        db.insert_delivery_to_table(username=user, timeslot_id=timeslot_id)


def exit_gracefully(*args):
    global consumer
    consumer.join(0.1)
    db.con.close()

    exit(0)


app.include_router(router)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    consumer = Thread(target=queue_consumer)
    consumer.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)






