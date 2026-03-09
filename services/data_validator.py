from schemas.input_schemas import FormOrderInput
from db.classes import Shop
from services.geocoder import geocode_address, GeocodingError
from datetime import datetime
from math import sqrt # TEMP

MAX_DISTANCE_KM = 50.0


class ValidationError(Exception):
    """Custom exception for business logic failures."""
    pass


def validate_and_prepare_order(order_request: FormOrderInput, db_session) -> dict:
    """
    Runs a validator after pydantic on the criteria below.
    If valid, returns an order entry as a clean dictionary.
    Checks:
    1. Specified shop exists
    2. ...
    ...
    n. ...
    """
    # FILL CHECKS ^^^
    shop = db_session.query(Shop).filter(Shop.shopId == order_request.shopId).first()

    if not shop:
        raise ValidationError(f"Shop ID {order_request.shopId} does not exist.")

    inittime = datetime.now()
    try:
        order_lat, order_lon = geocode_address(order_request.address)
    except GeocodingError as e:
        raise ValidationError(f"Geocoding failed: {str(e)}")
    distance = mock_calculate_distance(shop.latitude, shop.longitude, order_lat, order_lon)

    # if order_request.endTime < shop.openingTime + route.time or if order_request.endTime < inittime + route.time

    if order_request.startTime.time() < shop.openingTime or order_request.endTime.time() > shop.closingTime:
        raise ValidationError("Order time interval outside shop's operating hours.")

    if distance > MAX_DISTANCE_KM:
        raise ValidationError(f"Order is {distance} km away. Max allowed is {MAX_DISTANCE_KM} km.")

    return {
        "shopId": order_request.shopId,
        "type": order_request.type,
        "address": order_request.address,
        "startTime": order_request.startTime,
        "endTime": order_request.endTime,
        "latitude": order_lat,
        "longitude": order_lon,
        "initTime": inittime,
        "itemInfo": order_request.itemInfo,
        "driverInfo": order_request.driverInfo
    }


def mock_calculate_distance(lat1, lon1, lat2, lon2):
    """Temporary mock function for distance calculation"""
    # the distance will be larger than straight-line, calculated by OSM
    return sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 111