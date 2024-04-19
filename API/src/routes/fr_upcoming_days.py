from fastapi import APIRouter, Query, Path, HTTPException, Depends
from pydantic import BaseModel, validator
from typing import Optional  # Import Optional
from datetime import datetime, timedelta
import requests

from bearer_token.token import get_current_user

router = APIRouter()

# Define a Pydantic model for the response
class ErrorResponse(BaseModel):
    detail: str


def calculate_firerisk(days, longitude, latitude):
        try:
            response = requests.get('http://logic:2000/api/v1/fireriskUpcomingDays', params={'days': days, 'longitude': longitude, 'latitude': latitude})
            if response.status_code == 200:
                return response.json()
            else:
                return "Received non-200 response code."
        except Exception as e:
            return f"Error occurred: {e}"



@router.get("/v1/fireriskUpcomingDays", responses={
    404: {"model": ErrorResponse, "description": "firerisk not found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(days: Optional[int] = Query(None, description="This parameter is the time delta"),
                       longitude: Optional[float] = Query(None, description="This parameter is the longitude for the location"),
                       latitude: Optional[float] = Query(None, description="This parameter is the latitude for the location")):

    return calculate_firerisk(days, longitude, latitude)


@router.get("/v2/fireriskUpcomingDays")
async def get_firerisk_with_authorization(
        days: Optional[int] = Query(None, description="Time delta"),
        longitude: Optional[float] = Query(None, description="Longitude"),
        latitude: Optional[float] = Query(None, description="Latitude"),
        current_user: str = Depends(get_current_user)):
    
    return calculate_firerisk(days, longitude, latitude)


# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/fireriskUpcomingDays/?days=3&longitude=60.39299&latitude=5.32415