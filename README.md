# TalkGuest Analytics

A web-based hospitality data processing and visualization platform. Upload Excel files with guest, reservation, and invoice data, then analyze occupancy and revenue metrics with interactive charts.

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (React.js)                 │
│  - TailwindCSS styling                          │
│  - D3.js visualizations                         │
│  - File upload with drag & drop                 │
└──────────────────┬──────────────────────────────┘
                   │ REST API
                   │ (JSON data transfer)
┌──────────────────▼──────────────────────────────┐
│              Backend (Python Flask)              │
│  - RESTful API endpoints                        │
│  - Pandas/NumPy data transformation             │
│  - Bilingual support (PT/EN input files)        │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│          ETL Service                             │
│  - Guest/reservation data processing            │
│  - Occupancy & revenue report generation        │
│  - Excel file exports                           │
└─────────────────────────────────────────────────┘
```

## Project Structure

```
├── backend/                    # Python Flask API
│   ├── routers/               # API endpoint modules
│   │   ├── upload.py          # File upload endpoints
│   │   ├── process.py         # ETL processing endpoints
│   │   ├── results.py         # Results retrieval endpoints
│   │   └── download.py        # Excel download endpoints
│   ├── services/              # Business logic
│   │   └── etl_service.py     # Core ETL processing
│   ├── tests/                 # Unit tests
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend container
│   └── README.md              # Backend documentation
│
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── charts/        # D3.js chart components
│   │   │   ├── UploadTab.js   # File upload interface
│   │   │   ├── OccupancyTab.js # Occupancy visualizations
│   │   │   └── RevenueTab.js  # Revenue visualizations
│   │   ├── utils/
│   │   │   └── api.js         # API client
│   │   └── App.js             # Main application
│   ├── package.json           # Node dependencies
│   ├── Dockerfile             # Frontend container
│   └── README.md              # Frontend documentation
│
├── data/                       # Data directories
│   ├── raw/                   # Input files
│   └── processed/             # Output files
│
├── docker-compose.yml          # Production orchestration
├── docker-compose.tests.yml    # Test orchestration
└── README.md                   # This file
```

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000/api
```

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

## Running Tests

### Using Docker

```bash
docker-compose -f docker-compose.tests.yml up --build --abort-on-container-exit
```

### Local Testing

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
cd frontend
npm test
```

## API Endpoints

### Health
- `GET /api/health` - Service health check

### File Upload
- `POST /api/upload/guests` - Upload guests file
- `POST /api/upload/reservations` - Upload reservations file
- `POST /api/upload/invoices` - Upload invoices file (optional)
- `GET /api/upload/status` - Get upload status
- `DELETE /api/upload/<type>` - Remove uploaded file
- `DELETE /api/upload/clear` - Clear all uploads

### Processing
- `POST /api/process` - Run ETL pipeline
- `GET /api/process/status` - Get processing status

### Results
- `GET /api/results` - Get all results
- `GET /api/results/occupancy` - Get occupancy data
- `GET /api/results/revenue` - Get revenue data

### Downloads
- `GET /api/download/occupancy` - Download occupancy Excel
- `GET /api/download/revenue` - Download revenue Excel
- `GET /api/download/all` - Download combined report

## Features

### Data Processing
- Automatic language detection (Portuguese/English reservation files)
- Booking.com commission adjustment (+1.4%)
- Test entry filtering
- Duplicate detection and removal
- Zero-value reservation filtering
- Property grouping by configuration
- IVA/VAT calculation (4% Azores, 6% mainland)

### Visualizations
- **Occupancy Tab**
  - Bar charts: Nights by property, Person-nights by property
  - Pie charts: Nationality distribution
  - Data tables: Detailed breakdowns

- **Revenue Tab**
  - Bar charts: Revenue by property
  - Pie charts: Revenue breakdown (net, commission, VAT)
  - Grouped bar charts: Net vs commission comparison
  - Invoice comparison (when available)

### Reports
- Occupancy Report (Excel)
  - General statistics
  - Per-property nationality breakdown
- Revenue Report (Excel)
  - Summary totals
  - Property-level breakdown
  - Detailed calculations
  - Invoice comparison (when available)

## Input File Formats

### Guests File (Portuguese)
| Column | Description |
|--------|-------------|
| Nome | Guest name |
| Pais | Country |
| Email | Email (optional) |
| Telefone | Phone (optional) |

### Reservations File (Portuguese or English)
Supports both Portuguese and English column headers. Key columns:
- Reservation ID, Guest name, Property
- Check-in/Check-out dates, Nights
- Adults, Children
- Channel, Commission, Value

### Invoices File (Portuguese, Optional)
| Column | Description |
|--------|-------------|
| Documento | Invoice ID |
| Tipo Item | Item type (filter for "Estadia") |
| Total Documento | Total value |
| Total Base Incidência | Base amount |
| Total Do IVA | VAT amount |
| Alojamento | Property |
| Anulado | Cancelled flag |

## Environment Variables

### Backend
- `PORT` - Server port (default: 5000)
- `FLASK_DEBUG` - Enable debug mode

### Frontend
- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:5000/api)

## Technology Stack

- **Backend**: Python 3.11, Flask, Pandas, NumPy
- **Frontend**: React 18, D3.js, TailwindCSS
- **Testing**: Pytest, Jest, React Testing Library
- **Containerization**: Docker, Docker Compose

## License

MIT License