# triggers:
# DONE immediately upon startup if no orders assigned!!!
# DONE once every minute (check urgency)
#      when order added with endTime < datetime.now() + buffer
#      when end time of potential route is near endTime of last order in potential route

import asyncio
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.classes import Order, Driver
from services.routing_engine import run_routing_solver


async def dispatcher_loop():
    """Background daemon running in FastAPI."""
    print("Dispatcher daemon started.")
    while True:
        db = SessionLocal()
        try:
            evaluate_and_trigger(db)
        except Exception as e:
            print(f"Dispatcher error: {e}")
        finally:
            db.close()
        await asyncio.sleep(60)


def evaluate_and_trigger(db: Session):
    unlocked_orders = db.query(Order).filter(Order.status.in_([0, 1])).all()

    if not unlocked_orders:
        return

    urgent_pending = [o for o in unlocked_orders if o.type in [1, 2] and o.status == 0]

    normal_pending = [o for o in unlocked_orders if o.status == 0]

    if urgent_pending or len(normal_pending) >= 5:
        print(f"Routing orders... Pending: {len(normal_pending)}, Urgent: {len(urgent_pending)}")

        active_drivers = db.query(Driver).all()

        run_routing_solver(db, unlocked_orders, active_drivers)