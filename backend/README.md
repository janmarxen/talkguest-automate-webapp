# TalkGuest Backend API

Flask-based REST API for hospitality data processing and analysis.

## Features

- File upload endpoints for XLSX data (guests, reservations, invoices)
- ETL processing pipeline with bilingual support (Portuguese/English)
- Results API with occupancy and revenue analysis
- Excel report download endpoints

## API Endpoints

### Health
- `GET /api/health` - Health check

### Upload
- `POST /api/upload/guests` - Upload guests file
- `POST /api/upload/reservations` - Upload reservations file  
- `POST /api/upload/invoices` - Upload invoices file (optional)
- `GET /api/upload/status` - Get upload status
- `DELETE /api/upload/<type>` - Delete uploaded file
- `DELETE /api/upload/clear` - Clear all uploads

### Process
- `POST /api/process` - Run ETL pipeline
- `GET /api/process/status` - Get processing status

### Results
- `GET /api/results` - Get all results
- `GET /api/results/occupancy` - Get occupancy data
- `GET /api/results/revenue` - Get revenue data
- `GET /api/results/summary` - Get processing summary

### Download
- `GET /api/download/occupancy` - Download occupancy Excel
- `GET /api/download/revenue` - Download revenue Excel
- `GET /api/download/all` - Download combined report

## Development

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run development server
```bash
python app.py
```

### Run tests
```bash
pytest
```

## Docker

Build and run:
```bash
docker build -t talkguest-api .
docker run -p 5000:5000 talkguest-api
```
