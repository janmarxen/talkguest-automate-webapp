# TalkGuest Frontend

React-based frontend for TalkGuest Analytics with D3.js visualizations.

## Features

- File upload with drag & drop support
- Real-time processing status
- Interactive D3.js visualizations
  - Bar charts for property comparisons
  - Pie charts for nationality and revenue distribution
  - Grouped bar charts for multi-metric comparisons
- Excel report downloads
- TailwindCSS styling

## Tabs

1. **Upload & Process** - Upload XLSX files and trigger ETL processing
2. **Occupancy** - View occupancy metrics with nationality breakdowns
3. **Revenue** - Analyze revenue with commission and VAT breakdowns

## Development

### Install dependencies
```bash
npm install
```

### Start development server
```bash
npm start
```

### Run tests
```bash
npm test
```

### Build for production
```bash
npm run build
```

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: `http://localhost:5000/api`)

## Docker

Build and run:
```bash
docker build -t talkguest-frontend .
docker run -p 3000:3000 talkguest-frontend
```
