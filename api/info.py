from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def get_system_health():
    """GET call: returns services' and external APIs' status."""
    return {
        # "database": "mock online",
        # "yandex_api": "mock online",
        # "osm_engine": "mock online"
    }