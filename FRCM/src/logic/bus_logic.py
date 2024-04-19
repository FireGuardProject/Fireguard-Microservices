from datetime import timedelta, datetime
from fastapi import FastAPI
import requests
import json

from datamodel.model import FireRiskPrediction, Location, WeatherData, Observations, Forecast
from data_harvesting.client import WeatherDataClient
import FRC_service.compute
from data_harvesting.client_met import METClient
from data_harvesting.extractor_met import METExtractor


class FireRiskAPI:

    def __init__(self, client: WeatherDataClient):
        self.client = client
        self.timedelta_ok = timedelta(days=1) # TODO: when during a day is observations updated? (12:00 and 06:00)
        # TODO (NOTE): Short term forecast updates every 3rd hour with long term forecast every 12th hour at 12:00 and 06:00
        self.interpolate_distance = 720

    def compute(self, wd: WeatherData) -> FireRiskPrediction:
        return FRC_service.compute.compute(wd)
    

    def compute_previous_days(self, location: Location, delta: timedelta) -> FireRiskPrediction: 
        time_now = datetime.now()
        start_time = time_now - delta

        # request to: dataharvesting microservice
        observations = self.client.fetch_observations(location, start=start_time, end=time_now)
        forecast = self.client.fetch_forecast(location, start_time, time_now)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction 

    def compute_upcoming_days(self, location: Location, delta: timedelta) -> FireRiskPrediction: 
        time_now = datetime.now()
        end_time = time_now + delta
        observations = self.client.fetch_observations(location, start=time_now, end=end_time)
        forecast = self.client.fetch_forecast(location, time_now, end_time)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction

    def compute_specific_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        time_now = datetime.now()
        #databaselogic 
      
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location, start, end)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        
        prediction = self.compute(wd)
        return prediction 

    def compute_after_start_date(self, location: Location, start: datetime, delta: timedelta) -> FireRiskPrediction:
        time_now = datetime.now()
        end = start + delta
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location, start, end)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction

    def compute_before_end_date(self, location: Location, end: datetime, delta: timedelta) -> FireRiskPrediction:
        time_now = datetime.now()
        start = end - delta
        observations = self.client.fetch_observations(location, start=start, end=end)
        forecast = self.client.fetch_forecast(location, start, end)
        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)
        prediction = self.compute(wd)
        return prediction
    

met_extractor = METExtractor()
# TODO: maybe embed extractor into client
met_client = METClient(extractor=met_extractor)
frc = FireRiskAPI(client=met_client)

app = FastAPI()
@app.get("/api/v1/fireriskPreviousDays")
def fire_risk_previous_days(days: int, longitude: float, latitude: float):
    time_delta = timedelta(days=days)
    location1 = Location(longitude=float(longitude), latitude=float(latitude))
    result = frc.compute_previous_days(location=location1, delta=time_delta)
    return result

@app.get("/api/v1/fireriskSpecificPeriod")
def fire_risk_specific_period(start_date: str, end_date: str, longitude: float, latitude: float):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    location1 = Location(longitude=float(longitude), latitude=float(latitude))
    result = frc.compute_specific_period(location=location1, start=start, end=end)
    return result


@app.get("/api/v1/fireriskUpcomingDays")
def fire_risk_upcoming_days(days: int, longitude: float, latitude: float):
    delta = timedelta(days=days)
    location1 = Location(longitude=float(longitude), latitude=float(latitude))
    result = frc.compute_upcoming_days(location=location1, delta=delta)
    return result

@app.get("/api/v1/fireriskBeforeEndDate")
def fire_risk_compute_before_end_date(end_date, days, longitude, latitude):
    delta = timedelta(days=int(days))
    location = Location(longitude=longitude, latitude=latitude)
    end = datetime.fromisoformat(end_date)
    result = frc.compute_before_end_date(location, end, delta)
    return result


@app.get("/api/v1/fireriskAfterStartDate")
def fire_risk_compute_before_end_date(start_date, days, longitude, latitude):
    delta = timedelta(days=int(days))
    location = Location(longitude=longitude, latitude=latitude)
    start = datetime.fromisoformat(start_date)
    result = frc.compute_after_start_date(location, start, delta)
    return result


#    delta = timedelta(days=days)
#    location = Location(longitude=longitude, latitude=latitude)
#    start = datetime.fromisoformat(start_date)