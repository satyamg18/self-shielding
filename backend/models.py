from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    """A pre-registered genuine product, identified by its unique QR code."""
    __tablename__ = "products_v2"

    qr_code_id = Column(String, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    batch_number = Column(String, nullable=True)

    scans = relationship("Scan", back_populates="product")


class Scan(Base):
    """One scan event: who scanned which QR code, where, and when."""
    __tablename__ = "scans_v2"

    id = Column(Integer, primary_key=True, index=True)
    qr_code_id = Column(String, ForeignKey("products_v2.qr_code_id"), index=True, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    is_anomalous = Column(Boolean, default=False)
    packaging_confidence = Column(Float, nullable=True, default=1.0)
    telemetry_risk_score = Column(Float, nullable=True, default=0.0)
    trust_score = Column(Float, nullable=True, default=100.0)

    product = relationship("Product", back_populates="scans")


class Report(Base):
    """A customer report flagging a shop as a suspected counterfeit source."""
    __tablename__ = "reports_v2"

    id = Column(Integer, primary_key=True, index=True)
    qr_code_id = Column(String, index=True, nullable=False)
    shop_name = Column(String, nullable=False)
    shop_city = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
