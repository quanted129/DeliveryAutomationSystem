from fastapi import APIRouter
from api.orders import DbSession

router = APIRouter()

@router.get("/dashboard-stats")
def get_aggregate_stats(): # add db: DbSession later
    """GET call: returns information to be plotted using plt."""
    return {}