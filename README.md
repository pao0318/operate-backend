# Operate Backend

A FastAPI backend service with SSE (Server-Sent Events) support and Case Management APIs.

## Features

- **SSE Support**: Real-time event streaming for cross-application navigation
- **Case Management APIs**: Complete CRUD operations for case-related data
- **PostgreSQL Database**: Async database operations with SQLAlchemy
- **Alembic Migrations**: Database schema versioning
- **Clean Architecture**: Organized folder structure following best practices

## Project Structure

```
operate-backend/
├── app/
│   ├── api/
│   │   ├── endpoints/          # API route handlers
│   │   │   ├── health.py
│   │   │   ├── sse.py
│   │   │   ├── cases.py
│   │   │   ├── documents.py
│   │   │   └── ...
│   │   └── router.py           # Route aggregator
│   ├── core/
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # Database connection
│   │   └── exceptions.py       # Custom exceptions
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   │   └── sse_manager.py      # SSE connection manager
│   └── main.py                 # FastAPI application
├── alembic/
│   ├── versions/               # Migration files
│   └── env.py                  # Alembic configuration
├── requirements.txt
├── .env.example
├── alembic.ini
└── run.py                      # Application entry point
```

## Prerequisites

- Python 3.10+
- PostgreSQL 15+

## Installation

1. **Clone the repository**
   ```bash
   cd operate-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Create database**
   ```bash
   createdb operate_db
   ```

6. **Run migrations**
   ```bash
   alembic upgrade head
   ```

## Running the Application

### Development
```bash
python run.py
```
Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### SSE Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/sse` | SSE connection endpoint |
| POST | `/api/navigation` | Publish navigation events |
| GET | `/api/sse/health` | SSE service health |

### Case Management Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/available-services` | Get all available services |
| GET | `/api/case/{caseId}` | Get case details |
| GET | `/api/case/{caseId}/documents` | Get case documents |
| GET | `/api/case/{caseId}/extracted-key-metrics` | Get extracted key metrics |
| GET | `/api/case/{caseId}/covenant-status` | Get covenant status |
| GET | `/api/case/{caseId}/quarterly-dscr` | Get quarterly DSCR |
| GET | `/api/case/{caseId}/quarter-by-quarter-financial-drivers` | Get financial drivers |
| GET | `/api/case/{caseId}/q3-highlights` | Get Q3 highlights |
| GET | `/api/case/{caseId}/fr-y14-schedule-template` | Get FR Y14 schedule template |
| GET | `/api/case/{caseId}/y14-detailed-findings` | Get Y14 detailed findings |
| GET | `/api/case/{caseId}/shipment-details` | Get shipment details |
| GET | `/api/case/{caseId}/operational-doc-scan-detailed-findings` | Get operational findings |
| GET | `/api/case/{caseId}/data-simulator-benefits` | Get data simulator benefits |

## Testing the APIs

```bash
# Health check
curl http://localhost:8000/api/health

# SSE health
curl http://localhost:8000/api/sse/health

# Get available services
curl http://localhost:8000/api/available-services

# Get case
curl http://localhost:8000/api/case/1

# Publish navigation event
curl -X POST http://localhost:8000/api/navigation \
  -H "Content-Type: application/json" \
  -d '{"action": "navigate", "target_app_id": "app1", "route": "/dashboard"}'
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_ENV` | Environment (development/production) | development |
| `APP_DEBUG` | Enable debug mode | true |
| `APP_PORT` | Application port | 8000 |
| `APP_HOST` | Application host | 0.0.0.0 |
| `DATABASE_URL` | PostgreSQL connection URL | - |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | * |

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base
```

## License

MIT
