from fastapi import FastAPI, HTTPException
from decouple import config
import requests
from requests.auth import HTTPBasicAuth

from utils import haversine


app = FastAPI()


@app.get("/api/search/{iata_source}/{iata_destiny}/{departure_date}")
def somente_ida(iata_source: str, iata_destiny: str, departure_date: str):
    validate_airports((iata_source, iata_destiny))
    flights = get_flights(iata_source, iata_destiny, departure_date)
    for flight in flights["options"]:
        # Filling price
        fare = flight["price"]["fare"]
        fee = 40
        if (new_fee:=fare*0.1) > fee:
            fee = new_fee

        total = fare + fee
        flight["price"]["fees"]=fee
        flight["price"]["total"]=total
        # Filling meta
        distance = get_distance((iata_source, iata_destiny))
        breakpoint()

    return flights["options"]


def get_distance(airports):
    distances = get_lat_long(airports)
    

def get_flights(iata_source, iata_destiny, departure_date):
    response = requests.get(
        f"http://stub.2xt.com.br/air/search/{config('API_KEY')}/"
        f"{iata_source}/{iata_destiny}/{departure_date}",
        auth=HTTPBasicAuth('test', 'tB7vlD')
    )
    return response.json()


def get_airports():
    response = requests.get(
        'http://stub.2xt.com.br/air/airports/qEbvlDxInweeAIjmOzEl9vKKKMrdkvLV',
        auth=HTTPBasicAuth('test', 'tB7vlD')
    )
    return response.json()


def get_lat_long(airports_codes):
    airports = get_airports()
    airports_list = []
    for airport_code in airports_codes:
        airports_list.append(
            {
                "{airport_code}":(
                    airports[airport_code]["lat"],airports[airport_code]["lan"]
                )
            }
        )

def validate_airports(airports_codes):
    airports = get_airports()
    for airport_code in airports_codes:
        if airport_code not in airports:
            raise HTTPException(
                status_code=400,
                detail=f"AIRPORT_{airport_code}_IS_INVALID_OR_NOT_FOUND"
            )