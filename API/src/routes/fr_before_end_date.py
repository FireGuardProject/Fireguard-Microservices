from fastapi import APIRouter, Query, Path, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import Optional  # Import Optional
from datetime import datetime, timedelta
import requests
#from frcm.logic.bus_logic import FireRiskAPI
#from frcm.datamodel.model import Location
#from frcm.data_harvesting.client_met import METClient
#from frcm.data_harvesting.extractor_met import METExtractor
from bearer_token.token import get_current_user

#met_extractor = METExtractor()
# TODO: maybe embed extractor into client
#met_client = METClient(extractor=met_extractor)
#frc = FireRiskAPI(client=met_client)

# Define a Pydantic model for the response


#def calculate_firerisk(end_date, days, longitude, latitude):
#    delta = timedelta(days=days)
#    location = Location(longitude=longitude, latitude=latitude)
#    end = datetime.fromisoformat(end_date)
#    FireRiskPrediction = frc.compute_before_end_date(location, end, delta)
#    return FireRiskPrediction

class ErrorResponse(BaseModel):
    detail: str

router = APIRouter()

def calculate_firerisk(end_date, days, longitude, latitude):
        try:
            print(f'Sending request for firerisk based on {days} previous days.')
            response = requests.get('http://logic:2000/api/v1/fireriskBeforeEndDate/', params={'end_date':end_date ,'days': days ,'longitude': longitude,'latitude': latitude})
            if response.status_code == 200:
                return response.json() # Should print "pong"
            else:
                return "Received non-200 response code."
        except Exception as e:
            return f"Error occurred: {e}"



@router.get("/v1/fireriskBeforeEndDate", responses={
    404: {"model": ErrorResponse, "description": "firerisk not found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(end_date: Optional[str] = Query(None, description="This parameter is the date to search to"),
                       days: Optional[int] = Query(None, description="This parameter is the time delta"),
                       longitude: Optional[float] = Query(None, description="This parameter is the longitude for the location"),
                       latitude: Optional[float] = Query(None, description="This parameter is the latitude for the location")):

    return calculate_firerisk(end_date, days, longitude, latitude)


@router.get("/v2/fireriskBeforeEndDate")
async def get_firerisk_with_authorization(
        end_date: Optional[str] = Query(None, description="Date to search to"),
        days: Optional[int] = Query(None, description="Time delta"),
        longitude: Optional[float] = Query(None, description="Longitude"),
        latitude: Optional[float] = Query(None, description="Latitude"),
        current_user: str = Depends(get_current_user)):

    return calculate_firerisk(end_date, days, longitude, latitude)

# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/fireriskBeforeEndDate/?end_date=2024-03-10&days=3&longitude=5.32415&latitude=60.39299