# WMS Backend

This is the backend service for the Warehouse Management System (WMS). It's built with FastAPI and PostgreSQL.

## Features

- JWT-based authentication
- Warehouse management
- Storage location management
- Inventory item management
- Stock movement tracking
- Barcode support

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database:
```bash
createdb wms
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=wms
SECRET_KEY=your-secret-key-here
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin
```

5. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

1. Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Development

### Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

### Testing

Run tests with pytest:
```bash
pytest
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API endpoints
│   ├── core/            # Core functionality
│   ├── crud/            # Database operations
│   ├── db/              # Database configuration
│   ├── models/          # SQLAlchemy models
│   └── schemas/         # Pydantic schemas
├── tests/               # Test files
├── .env                 # Environment variables
├── alembic.ini          # Alembic configuration
├── requirements.txt     # Project dependencies
└── README.md           # This file
``` 