from datetime import datetime

from fastapi import FastAPI, HTTPException
from decouple import config
import requests
from requests.auth import HTTPBasicAuth

from utils import haversine


app = FastAPI()


@app.get("/api/search/{iata_source}/{iata_destiny}/{departure_date}")
def somente_ida(iata_source: str, iata_destiny: str, departure_date: str):
    if iata_source == iata_destiny:
        raise HTTPException(
                status_code=400,
                detail=f"AIRPORTS_CODE_CANNOT_BE_EQUAL"
            )
    validate_airports((iata_source, iata_destiny))
    flights = get_flights(iata_source, iata_destiny, departure_date)
    for flight in flights["options"]:
        departure_time = datetime.strptime(flight["departure_time"], '%Y-%m-%dT%H:%M:%S')
        arrival_time = datetime.strptime(flight["arrival_time"], '%Y-%m-%dT%H:%M:%S')
        # Filling price
        fare = flight["price"]["fare"]
        fee = 40
        if (new_fee:=fare*0.1) > fee:
            fee = new_fee

        total = fare + fee
        flight["price"]["fees"] = fee
        flight["price"]["total"] = total
        # Filling meta
        distance = get_distance(iata_source, iata_destiny)
        flight["meta"]["range"] = distance
        cruise_speed = (
            distance/(arrival_time-departure_time).seconds
        ) * 3600
        flight["meta"]["cruise_speed_kmh"] = cruise_speed
        flight["meta"]["cost_per_km"] = distance/fare

    return flights["options"]


@app.get(
    "/api/search/{iata_source}/{iata_destiny}/{departure_date}/{arrival_date}"
)
def ida_e_volta(
    iata_source: str, iata_destiny: str, departure_date: str, arrival_date: str
):
    if iata_source == iata_destiny:
        raise HTTPException(
                status_code=400,
                detail=f"AIRPORTS_CODE_CANNOT_BE_EQUAL"
            )
    validate_airports((iata_source, iata_destiny))
    validate_dates(departure_date, arrival_date)
    departure_flights = get_flights(iata_source, iata_destiny, departure_date)
    arrival_flights = get_flights(iata_destiny, iata_source, arrival_date)
    return "asdasd"



def get_distance(iata_source, iata_destiny):
    distances = get_lat_long((iata_source, iata_destiny))
    distance = haversine(*distances[iata_source], *distances[iata_destiny])
    return distance


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
    airports_dict = {}
    for airport_code in airports_codes:
        airports_dict[f"{airport_code}"] = (
            airports[airport_code]["lat"],
            airports[airport_code]["lon"]
        )
        
        
    
    return airports_dict


def validate_airports(airports_codes):
    airports = get_airports()
    for airport_code in airports_codes:
        if airport_code not in airports:
            raise HTTPException(
                status_code=400,
                detail=f"AIRPORT_{airport_code}_IS_INVALID_OR_NOT_FOUND"
            )


def validate_dates(departure_date, arrival_date):
    departure_date = datetime.strptime(departure_date, '%Y-%m-%d')
    arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d')
    if arrival_date < departure_date:
        raise HTTPException(
                status_code=400,
                detail=f"DATE_ERRO"
            )


