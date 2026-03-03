from db.database import SessionLocal
from schemas.input_schemas import FormOrderInput
from services.data_validator import ValidationError, validate_and_prepare_order
from db.classes import Order


def test_ingestion_pipeline():

    mock_incoming_data = {
        "shopId": 1,
        "type": 1,
        "address": "пр. Победителей 111",
        "startTime": "2026-03-08T10:00:00",
        "endTime": "2026-03-08T12:00:00",
        "itemInfo": "Букет цветов",
        "driverInfo": "Не звонить, доставка-сюрприз"
    }

    db = SessionLocal()

    try:
        print("Running Pydantic validation...")
        clean_input = FormOrderInput(**mock_incoming_data)

        print("Running sanity checks...")
        validated_db_dict = validate_and_prepare_order(clean_input, db)

        print("Order successfully validated! Saving to database...")
        new_order = Order(**validated_db_dict)
        db.add(new_order)
        db.commit()
        print(f"Successfully created Order ID: {new_order.orderId}")

    except ValueError as e:  # Caught Pydantic structural errors
        print(f"Structural Data Error: {e}")
    except ValidationError as e:  # Caught custom logical errors
        print(f"Business Logic Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    test_ingestion_pipeline()