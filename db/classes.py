from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, Unicode, DateTime, Time, Boolean, ForeignKey
from db.database import Base


class Shop(Base):
    __tablename__ = "shops"
    shopId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    type = Column(Boolean)  # 0 - temporary, 1 - permanent
    name = Column(Unicode(255), unique=True)
    latitude = Column(Float(precision=8, decimal_return_scale=6))
    longitude = Column(Float(precision=9, decimal_return_scale=6))
    address = Column(Unicode)
    openingTime = Column(Time)
    closingTime = Column(Time)
    orders = relationship("Order", back_populates="shop")


class Driver(Base):
    __tablename__ = "drivers"
    driverId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(Unicode(255), unique=True)
    latitude = Column(Float(precision=8, decimal_return_scale=6))
    longitude = Column(Float(precision=9, decimal_return_scale=6))
    address = Column(Unicode)
    orders = relationship("Order", back_populates="driver")


class Order(Base):
    __tablename__ = "orders"
    orderId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    shopId = Column(Integer, ForeignKey("shops.shopId"))
    driverId = Column(Integer, ForeignKey("drivers.driverId"), nullable=True)
    type = Column(Integer)  # 0 - well-structured, 1 - one-sided, 2 - express, 3 - no time limit, 4 - invalid info
    status = Column(Integer, default=0)  # 0 - pending, 1 - assigned, 2 - en route, 3 - delivered, 4 - cancelled
    eta = Column(DateTime)
    routeSequence = Column(Integer)
    initTime = Column(DateTime)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    itemInfo = Column(Unicode)
    driverInfo = Column(Unicode)
    latitude = Column(Float(precision=8, decimal_return_scale=6))
    longitude = Column(Float(precision=9, decimal_return_scale=6))
    address = Column(Unicode)
    shop = relationship("Shop", back_populates="orders")
    driver = relationship("Driver", back_populates="orders")