# ParkSafe ANPR

A cloud-based Automatic Number Plate Recognition (ANPR) SaaS designed to eliminate hardware CapEx for parking lot operators. ParkSafe transforms existing CCTV networks and standard office PCs into intelligent edge-inference nodes, decoupling heavy computer vision processing from the cloud database.

> **Development Status: Work in Progress (Local Environment)** 
> The platform core (FastAPI backend, React dashboard) is actively being built and tested locally. The computer vision pipeline is currently simulated to allow for parallel backend development before production deployment.

## Core Architecture

* **Backend:** FastAPI (Python), SQLAlchemy, SQLite
* **Frontend:** React.js, Tailwind CSS
* **Data Contract:** Lightweight JSON payloads over HTTP to minimize local bandwidth reliance

## Implemented Features (Local)

* **Live Lot Monitoring:** Real-time visibility into active parking sessions and daily volume.
* **Manual Plate Overrides:** Immediate database correction via primary key (`session_id`) targeting to safely resolve misread dirty license plates without historical data collision.
* **Dashboard Analytics:** Revenue and parking volume calculation dynamically fetched from the local database.
* **JWT Authentication:** Secure admin endpoints and protected React route access.

## Development Roadmap

**Currently Completed:**
* Platform core, database schema, JWT auth, and React admin dashboard.
* Session CRUD operations, manual plate overrides, and UI state reconciliation.

**Current Focus (Active Sprint):**
* Payment gateway integration (Razorpay / UPI QR for exit fee calculation).

**Future Scope:**
* Edge Node integration (replacing the camera simulator with the live YOLOv26n OpenCV/OpenVINO pipeline) and production cloud deployment.

## Local Development Setup

### Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000 --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```