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


def calculate_firerisk(start_date, end_date, longitude, latitude):
        try:
            response = requests.get('http://logic:2000/api/v1/fireriskSpecificPeriod', params={'start_date': start_date, 'end_date': end_date, 'longitude': longitude, 'latitude': latitude})
            if response.status_code == 200:
                return response.json()
            else:
                return "Received non-200 response code."
        except Exception as e:
            return f"Error occurred: {e}"


def check_date(date_first, date_last):
    if date_first >= date_last:
        raise HTTPException(status_code=400, detail="The end date must be after the start date.")


@router.get("/v1/fireriskSpecificPeriod", responses={
    404: {"model": ErrorResponse, "description": "firerisk not found"},
    400: {"model": ErrorResponse, "description": "invalid input"}
})
async def get_firerisk(start_date: Optional[str] = Query(None, description="This parameter is the date to search from"),
                       end_date: Optional[str] = Query(None, description="This parameter is the date to search to"),
                       longitude: Optional[float] = Query(None, description="This parameter is the longitude for the location"),
                       latitude: Optional[float] = Query(None, description="This parameter is the latitude for the location")):
   
    # check_date(start_date, end_date)

    return calculate_firerisk(start_date, end_date, longitude, latitude)


@router.get("/v2/fireriskSpecificPeriod")
async def get_firerisk_with_authorization(
        start_date: Optional[str] = Query(None, description="Date to search from"),
        end_date: Optional[str] = Query(None, description="Date to search to"),
        longitude: Optional[float] = Query(None, description="Longitude"),
        latitude: Optional[float] = Query(None, description="Latitude"),
        current_user: str = Depends(get_current_user)):
    
    return calculate_firerisk(start_date, end_date, longitude, latitude)

# Bergen kordinater: 60.39299 5.32415

#URL EXAMPLE: http://127.0.0.1:8000/api/v1/fireriskSpecificPeriod/?start_date=2024-03-05&end_date=2024-03-15&longitude=5.32415&latitude=60.39299