# 🛡️ Self-Shielding

### AI-Driven Counterfeit Product Detection Platform

> A full-stack surveillance platform that detects counterfeit consumer goods by combining QR scan telemetry, geographic anomaly analysis, AI-powered packaging inspection, and crowd-sourced community reporting.

---

## Overview

Counterfeit consumer goods have evolved beyond poor-quality imitations. Modern counterfeiters replicate packaging, branding, batch numbers, expiry dates, and even genuine QR codes, making traditional visual verification ineffective.

**Self-Shielding** addresses this by shifting authentication from static QR verification to **behavioural anomaly detection + AI packaging analysis**. Rather than just validating whether a QR code exists, the system evaluates how that QR code behaves across locations and time, while simultaneously running AI vision checks on the product's physical appearance.

---

## Problem Statement

Conventional product verification systems rely on static QR codes that simply redirect users to a manufacturer's website.

This approach fails because counterfeiters often duplicate a genuine QR code across thousands of fake products. Every counterfeit product therefore appears authentic despite sharing the same identifier.

As a result:

- Consumers unknowingly purchase counterfeit products.
- Manufacturers suffer financial and reputational losses.
- Authorities receive counterfeit reports only after significant market damage.

---

## Proposed Solution

Self-Shielding introduces a **multi-layered verification system** combining:

### 1. Scan Telemetry Analysis
Every product scan contributes anonymous telemetry:
- QR Code Identifier
- Scan Timestamp
- Geographic Location (GPS + City)
- Scan Frequency

The backend continuously evaluates these records to detect abnormal scanning behaviour. For example, if the same QR code is scanned from multiple geographically distant cities, the system flags the product as potentially counterfeit.

### 2. AI Trust Score (6-Pillar Model)
Each scan generates a **Trust Score (0–100%)** computed from six pillars:

| Pillar | Weight | Description |
|---|---|---|
| Digital Signature | 30% | Cryptographic QR code validation |
| QR Validity | 20% | Code registered in manufacturer database |
| Packaging AI | 20% | Logo, font, colour, and print quality analysis |
| OCR Consistency | 10% | Expiry date and batch text verification |
| Scan Telemetry | 10% | Historical scan frequency and location patterns |
| Community Reports | 10% | Crowd-sourced retailer flagging |

### 3. Escalation Engine
Repeated customer reports against the same retailer automatically classify that location as a **Hot Zone**, enabling administrators to monitor counterfeit distribution patterns in real time.

---

## Key Features

### Consumer App — QR Scanner
- Live camera QR code scanning (jsQR)
- Manual QR code entry
- Behaviour-based counterfeit detection with escalating warnings (SAFE → WARNING → CAUTION → FAKE)
- AI Trust Score display with packaging confidence and telemetry risk metrics
- Automatic geolocation capture
- One-tap counterfeit reporting

### Community Reporting Portal
- Report suspicious retailers with QR code, shop name, city, GPS coordinates, and notes
- Auto-escalation to Hot Zone after 3+ reports on the same shop
- Context carry-over from scanner (pre-fills QR code)

### Business Surveillance Dashboard (Admin)
- Password-protected admin access
- Live scan statistics and AI confidence metrics
- Anomaly detection table with colour-coded severity levels
- Geographic hot-zone map (Leaflet + Carto dark tiles)
- Brand-wise genuine vs flagged scan distribution chart (Chart.js)
- Real-time escalation event ticker

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI (Python) |
| Database | PostgreSQL (production) / SQLite (local dev) |
| ORM | SQLAlchemy |
| Frontend | Vanilla HTML/CSS/JS |
| QR Scanning | jsQR |
| Maps | Leaflet.js + Carto |
| Charts | Chart.js |
| Fonts | JetBrains Mono, Archivo, Inter (Google Fonts) |
| Deployment | Vercel (Serverless Python) |

---

## Project Structure

```
self-shielding/
├── backend/
│   ├── main.py              # FastAPI application & all endpoints
│   ├── database.py          # DB engine, session, lazy init
│   ├── models.py            # SQLAlchemy ORM models (Product, Scan, Report)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── logic.py             # Anomaly detection & AI trust score engine
│   ├── seed.py              # Demo product seeder (6 products)
│   ├── seed_50.py           # Extended seeder (250 products, 30 brands)
│   └── requirements.txt     # Python dependencies
│
├── index.html               # Consumer scanner page
├── dashboard.html           # Admin surveillance dashboard
├── report.html              # Community reporting form
├── vercel.json              # Vercel deployment config
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/scan` | — | Scan a QR code, log telemetry, return trust score |
| `GET` | `/product/{qr_code_id}` | — | Retrieve product details |
| `POST` | `/report` | — | Submit a counterfeit retailer report |
| `GET` | `/stats` | Admin | Dashboard summary statistics |
| `GET` | `/anomalies` | Admin | Flagged QR codes with severity levels |
| `GET` | `/hotzones` | Admin | Aggregated retailer reports for map |
| `GET` | `/brand_volume` | Admin | Genuine vs flagged scans per brand |
| `GET` | `/api/health` | — | Health check |

---

## Local Setup

```bash
# Clone and enter the project
cd self-shielding

# Install dependencies
pip install -r backend/requirements.txt

# Seed the demo database
cd backend
python seed.py
python seed_50.py

# Run the server
uvicorn main:app --reload --port 8000
```

Then open `http://localhost:8000` in your browser.

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | No | PostgreSQL connection string (defaults to SQLite) |
| `ADMIN_KEY` | No | Dashboard password (defaults to `admin123`) |

---

## Deployment

The project is deployed on **Vercel** as a serverless Python function.

**Live URL:** [https://self-shielding.vercel.app](https://self-shielding.vercel.app)

---

## Future Scope

- Real-time Vision AI integration for live packaging photo analysis
- Dynamic time-window anomaly analysis
- Brand-specific detection thresholds
- Manufacturer analytics portal
- Counterfeit trend forecasting
- Mobile application support

---

## Team

Developed as a hackathon project to demonstrate how AI-powered behavioural analytics can strengthen counterfeit product detection and improve consumer trust.
