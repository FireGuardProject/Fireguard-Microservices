#dependencies
from fastapi import APIRouter, Query, Path, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import Optional  # Import Optional
from datetime import datetime, timedelta
import requests

from bearer_token.token import get_current_user

router = APIRouter()


#local imports
#from frcm.logic.bus_logic import FireRiskAPI
#from frcm.datamodel.model import Location
#from frcm.data_harvesting.client_met import METClient
#from frcm.data_harvesting.extractor_met import METExtractor

#need to be moved:
#met_extractor = METExtractor()
#met_client = METClient(extractor=met_extractor)
#frc = FireRiskAPI(client=met_client)

#def calculate_firerisk(days, longitude, latitude):
#    delta = timedelta(days=days)
#    location = Location(longitude=longitude, latitude=latitude)
#    FireRiskPrediction = frc.compute_previous_days(location, delta)
#    return FireRiskPrediction

# Define a Pydantic model for the response
class ErrorResponse(BaseModel):
    detail: str



def calculate_firerisk(days, longitude, latitude):
        try:
            print(f'Sending request for firerisk based on {days} previous days.')
            response = requests.get('http://logic:2000/api/v1/fireriskPreviousDays', params={'days': days, 'longitude': longitude, 'latitude': latitude})
            if response.status_code == 200:
                return response.json() # Should print "pong"
            else:
                return "Received non-200 response code."
        except Exception as e:
            return f"Error occurred: {e}"



@router.get("/v1/fireriskPreviousDays", responses={
    404: {"model": ErrorResponse, "description": "firerisk not found"},
    400: {"model": ErrorResponse, "description": "invalid input, better luck next time noob!"},
})
async def get_firerisk(days: Optional[int] = Query(None, description="This parameter is the time delta"),
                       longitude: Optional[float] = Query(None, description="This parameter is the longitude for the location"),
                       latitude: Optional[float] = Query(None, description="This parameter is the latitude for the location")):
    return calculate_firerisk(days, longitude, latitude)


@router.get("/v2/fireriskPreviousDays")
async def get_firerisk_with_authorization(
        days: Optional[int] = Query(None, description="Time delta"),
        longitude: Optional[float] = Query(None, description="Longitude"),
        latitude: Optional[float] = Query(None, description="Latitude"),
        current_user: str = Depends(get_current_user)):
    return calculate_firerisk(days, longitude, latitude)


# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/fireriskPreviousDays/?days=3&longitude=5.32415&latitude=60.39299

