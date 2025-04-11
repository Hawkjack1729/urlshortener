# URL Shortener API

A robust URL shortener API built with FastAPI and PostgreSQL.

## Features

- Shorten long URLs to easily shareable short links
- Custom short codes (optional)
- URL redirection
- URL statistics (creation date, access count, last accessed)
- API documentation with Swagger UI
- Containerized environment with Docker

## Project Structure

The project follows a clean architecture pattern with separation of concerns:

```
url_shortener/
├── app/                  # Application package
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core functionality (config, security, exceptions)
│   ├── db/               # Database models and repositories
│   ├── models/           # SQLAlchemy ORM models
│   └── schemas/          # Pydantic schemas for request/response validation
├── migrations/           # Alembic migrations
├── .env                  # Environment variables (not in version control)
├── .env.example          # Example environment variables
├── docker-compose.yml    # Docker Compose configuration
└── Dockerfile            # Docker configuration
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Docker & Docker Compose (optional)

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file (use `.env.example` as a template):

```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration.

6. Start the application:

```bash
uvicorn app.main:app --reload
```

### Using Docker

1. Clone the repository.

2. Create a `.env` file (use `.env.example` as a template).

3. Start the containers:

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## API Endpoints

### Shorten URL

```
POST /api/v1/shorten
```

Request body:

```json
{
  "url": "https://example.com/very/long/url",
  "custom_code": "mycode" // Optional
}
```

Response:

```json
{
  "short_code": "mycode",
  "short_url": "http://localhost:8000/mycode",
  "original_url": "https://example.com/very/long/url"
}
```

### Redirect to Original URL

```
GET /{short_code}
```

This endpoint redirects to the original URL.

### Get URL Information

```
GET /api/v1/info/{short_code}
```

Response:

```json
{
  "short_code": "mycode",
  "short_url": "http://localhost:8000/mycode",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2023-09-01T12:00:00",
  "last_accessed": "2023-09-01T13:00:00",
  "access_count": 5
}
```

## Testing

Run the tests:

```bash
pytest
```

## License

MIT
