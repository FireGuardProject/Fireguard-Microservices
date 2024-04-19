from fastapi import APIRouter
from routes import fr_previous_days, fr_specific_period, fr_upcoming_days, fr_after_start_date, fr_upcoming_days, fr_before_end_date
from bearer_token import route

api_router = APIRouter()
api_router.include_router(fr_previous_days.router, prefix="", tags=["fr_previous_days"])
api_router.include_router(route.router, prefix="", tags=["bearer_token_route"])
api_router.include_router(fr_after_start_date.router, prefix="", tags=["fr_from_startdate"])
api_router.include_router(fr_upcoming_days.router, prefix="", tags=["fr_upcoming_days"])
api_router.include_router(fr_before_end_date.router, prefix="", tags=["fr_before_end_date"])
api_router.include_router(fr_specific_period.router, prefix="", tags=["fr_specific_period"])