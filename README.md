# FastAPI Docker Setup

A FastAPI application with Docker support for both development and production environments.

## Project Structure

```
.
├── app/
│   └── main.py          # FastAPI application
├── Dockerfile           # Production Dockerfile
├── Dockerfile.dev       # Development Dockerfile
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file

```

## Quick Start

### Development

1. Copy the environment file:
   ```bash
   cp .env.dev.example .env.dev
   ```

2. Start the development container:
   ```bash
   docker-compose up app-dev
   ```

   The API will be available at `http://localhost:8000`

3. For development with auto-reload, the code is mounted as a volume, so changes will be reflected automatically.

### Production

1. Copy the environment file:
   ```bash
   cp .env.prod.example .env.prod
   ```

2. Start the production container:
   ```bash
   docker-compose --profile production up app-prod
   ```

   The API will be available at `http://localhost:8001`

### Build and Run Manually

#### Development
```bash
docker build -f Dockerfile.dev -t fastapi-dev .
docker run -p 8000:8000 -v $(pwd)/app:/app/app fastapi-dev
```

#### Production
```bash
docker build -t fastapi-prod .
docker run -p 8000:8000 fastapi-prod
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Environment Variables

- `ENVIRONMENT` - Current environment (development/production)
- `DEBUG` - Debug mode flag

## Notes

- Development mode includes auto-reload for faster iteration
- Production mode uses multiple workers for better performance
- Volumes are mounted in development for live code updates
- Production service runs on port 8001 to avoid conflicts with dev

# cat-or-dog-classifier
