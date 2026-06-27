"""
The heart of the project: deciding whether a QR code's scan pattern is
physically plausible for one genuine product, or a sign of mass duplication.

Rule (all-time, no rolling window):
  - A genuine product can be scanned a few times by curious customers in
    ONE city/shop. Each scan past the first nudges the warning level up:
        scan 1            -> SAFE      (green)
        scan 2            -> WARNING   (yellow)
        scan 3            -> CAUTION   (orange)
        scan 4 and beyond -> FAKE      (red)
    This gives an escalating signal instead of a hard on/off flip.
  - The moment the SAME QR code is ever scanned from a SECOND distinct
    city, that's immediate proof of duplication — one physical bottle
    cannot be in two cities. Jumps straight to FAKE regardless of count.
"""

from sqlalchemy.orm import Session
import random

import models

SAME_CITY_SCAN_LIMIT = 3  # scans 1..3 in one city are SAFE/WARNING/CAUTION; 4+ is FAKE
REPORT_ESCALATION_THRESHOLD = 3

# scan_count -> level, for the same-city case (multi-city always overrides to FAKE)
LEVEL_BY_SAME_CITY_COUNT = {
    1: "SAFE",
    2: "WARNING",
    3: "CAUTION",
}


def evaluate_ai_trust_score(qr_code_id: str, scan_count: int, unique_cities: int) -> dict:
    """
    Simulates the AI Trust Score based on 6 pillars:
    Digital signature (30), QR validity (20), Packaging AI (20), OCR consistency (10),
    Previous scans (10), User reports (10).
    """
    is_fake = "FAKE" in qr_code_id.upper() or unique_cities >= 2 or scan_count > SAME_CITY_SCAN_LIMIT
    
    signature_valid = True
    qr_valid = True
    
    if is_fake:
        packaging_confidence = round(random.uniform(0.35, 0.60), 3)
        logo_match = random.random() > 0.3 # Sometimes fake logo is good
        ocr_match = random.random() > 0.4
        telemetry_risk = round(random.uniform(0.70, 0.99), 3)
    else:
        packaging_confidence = round(random.uniform(0.92, 0.99), 3)
        logo_match = True
        ocr_match = True
        telemetry_risk = round(random.uniform(0.01, 0.12), 3)
        
    score = 0
    if signature_valid: score += 30
    if qr_valid: score += 20
    score += int(packaging_confidence * 20)
    if ocr_match: score += 10
    
    scan_pts = max(0, 10 - ((scan_count - 1) * 3))
    score += scan_pts
    
    report_pts = 10 if not is_fake else 0
    score += report_pts
    
    return {
        "trust_score": float(score),
        "packaging_confidence": packaging_confidence,
        "telemetry_risk": telemetry_risk,
        "ocr_match": ocr_match,
        "logo_match": logo_match,
        "signature_valid": signature_valid,
        "qr_valid": qr_valid
    }


def get_all_scans(db: Session, qr_code_id: str):
    """Every scan ever logged for this QR code — no time window."""
    return db.query(models.Scan).filter(models.Scan.qr_code_id == qr_code_id).all()


def evaluate_anomaly(db: Session, qr_code_id: str):
    """
    Returns (level, scan_count, unique_cities, trigger) for a given QR code,
    based on ALL scans it has ever received.

    level is one of: "SAFE", "WARNING", "CAUTION", "FAKE"
    trigger is one of: None, "multi_city", "city_limit"
    """
    scans = get_all_scans(db, qr_code_id)
    scan_count = len(scans)

    # normalize city names for comparison so "Delhi" and "delhi" count as one
    normalized_cities = {s.city.strip().lower() for s in scans if s.city and s.city.strip()}
    unique_cities = len(normalized_cities)

    if unique_cities >= 2:
        return "FAKE", scan_count, unique_cities, "multi_city"

    if scan_count > SAME_CITY_SCAN_LIMIT:
        return "FAKE", scan_count, unique_cities, "city_limit"

    level = LEVEL_BY_SAME_CITY_COUNT.get(scan_count, "SAFE")
    return level, scan_count, unique_cities, None
