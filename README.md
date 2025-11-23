# 🐱 Cat or Dog Classifier 🐶

A machine learning web application that classifies images as either cats or dogs using a pre-trained deep learning model. Built with FastAPI, TensorFlow, and MLflow for tracking classifications.

**Model Credit**: This application uses a pre-trained model from [Kaggle - Cats vs Dogs Classifier by wafaaelhusseini](https://www.kaggle.com/models/wafaaelhusseini/cats-vs-dogs-classifier).

## 🌟 Features

- **Interactive Web UI**: Beautiful, responsive interface for uploading and classifying images
- **RESTful API**: Easy-to-use API endpoint for integration with other applications
- **MLflow Integration**: Automatic logging of all classifications with metrics and artifacts

## 🚀 Live Demo

- **Web Application**: [https://cod.borenmon.dev](https://cod.borenmon.dev)
- **API Documentation**: [https://cod.borenmon.dev/docs](https://cod.borenmon.dev/docs)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13+** (or Python 3.10+)
- **Docker** and **Docker Compose** (for containerized deployment)
- **Git** (for cloning the repository)

## 🛠️ Installation

### Option 1: Docker (Recommended)

This is the easiest way to get started with the project.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/BorenMon/cat-or-dog-classifier.git
cd cat-or-dog-classifier
```

#### Step 2: Create Environment File

Create a `.env` file in the root directory:

```bash
cp .env.example .env  # If you have an example file
# Or create manually:
touch .env
```

Add the following to `.env`:

```env
ENVIRONMENT=development
FASTAPI_PORT=8888
MLFLOW_UI_PORT=5555
```

**Port Configuration**:
- `FASTAPI_PORT`: External port for FastAPI (default: 8888)
- `MLFLOW_UI_PORT`: External port for MLflow UI (default: 5555)
- Internal ports (8000 for FastAPI, 5000 for MLflow) remain fixed

#### Step 3: Build and Run with Docker Compose

```bash
# Build and start the containers
docker compose up --build

# Or run in detached mode
docker compose up -d --build
```

The application will be available at:
- **Web UI**: http://localhost:${FASTAPI_PORT} (default: 8888)
- **API Docs**: http://localhost:${FASTAPI_PORT}/docs (default: 8888)
- **MLflow UI**: http://localhost:${MLFLOW_UI_PORT} (default: 5555)

**Note**: Ports are configurable via environment variables in `.env`. If you change `FASTAPI_PORT` or `MLFLOW_UI_PORT`, use those values instead.

#### Step 4: Stop the Application

```bash
docker compose down
```

### Option 2: Local Development Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/BorenMon/cat-or-dog-classifier.git
cd cat-or-dog-classifier
```

#### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Ensure Model File Exists

Make sure the pre-trained model file `cats_dogs_finetuned_FT.keras` is in the root directory.

#### Step 5: Run the Application

```bash
# Start MLflow UI (in a separate terminal)
mlflow ui --port 5000 --host 0.0.0.0 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns

# Start FastAPI server (in another terminal)
fastapi dev main.py --host 0.0.0.0 --port 8000
```

Or use the production mode:

```bash
fastapi run main.py --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000

## 📁 Project Structure

```
COD/
├── main.py                 # FastAPI application and API endpoints
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose configuration
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
├── cats_dogs_finetuned_FT.keras  # Pre-trained model file
├── mlflow.db             # MLflow SQLite database
├── mlruns/               # MLflow experiment runs and artifacts
└── ui/                   # Frontend files
    ├── index.html        # Main HTML file
    ├── script.js         # JavaScript for UI interactions
    └── style.css         # CSS styling
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Environment: development or production
ENVIRONMENT=development

# Port Configuration (for Docker Compose)
FASTAPI_PORT=8888      # External port for FastAPI web server
MLFLOW_UI_PORT=5555   # External port for MLflow UI

# Optional: Add other configuration variables as needed
```

**Port Configuration Notes**:
- `FASTAPI_PORT`: Maps to internal port 8000 (default: 8888)
- `MLFLOW_UI_PORT`: Maps to internal port 5000 (default: 5555)
- These ports are only used when running with Docker Compose
- For local development, use the default ports (8000 for FastAPI, 5000 for MLflow)

### Model Configuration

The model file `cats_dogs_finetuned_FT.keras` should be placed in the root directory. If you need to use a different model:

1. Update the `MODEL_PATH` variable in `main.py`
2. Ensure the model is compatible with TensorFlow/Keras

## 📖 Usage

### Web Interface

1. Open your browser and navigate to the web UI:
   - **Docker**: http://localhost:${FASTAPI_PORT} (default: 8888)
   - **Local**: http://localhost:8000
2. Click "Choose File" or drag and drop an image
3. Click "Classify Image" to get the prediction
4. View the results with confidence scores and probabilities

### API Usage

#### Classify an Image

```bash
curl -X POST "http://localhost:8000/api" \
  -F "file=@path/to/your/image.jpg"
```

#### Response Example

```json
{
  "classification": "cat",
  "confidence": 0.9234,
  "probabilities": {
    "cat": 0.9234,
    "dog": 0.0766
  }
}
```

#### Python Example

```python
import requests

url = "http://localhost:8000/api"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
result = response.json()
print(result)
```

#### JavaScript Example

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📚 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The API documentation includes:
- All available endpoints
- Request/response schemas
- Try-it-out functionality
- Link back to the web UI

## 🔍 MLflow Tracking

All predictions are automatically logged to MLflow with:
- **Metrics**: Confidence scores, probabilities
- **Parameters**: Classification result, model path, image format
- **Artifacts**: Input images for each prediction

Access MLflow UI at:
- **Development**: http://localhost:5000
- **Docker**: http://localhost:${MLFLOW_UI_PORT} (default: 5555)

**Note**: The MLflow port in Docker is configurable via the `MLFLOW_UI_PORT` environment variable in your `.env` file.

## 🐳 Docker Commands

### Build the Image

```bash
docker compose build
```

### Start Services

```bash
docker compose up -d
```

### View Logs

```bash
docker compose logs -f
```

### Stop Services

```bash
docker compose down
```

### Rebuild After Changes

```bash
docker compose up --build -d
```

**Note**: The docker-compose.yml uses environment variables for port configuration. Make sure your `.env` file includes `FASTAPI_PORT` and `MLFLOW_UI_PORT` if you want to customize the ports.

## 🚀 Production Deployment

### Using Docker Compose

1. Set environment to production in `.env`:

```env
ENVIRONMENT=production
FASTAPI_PORT=8888
MLFLOW_UI_PORT=5555
```

2. Build and run:

```bash
docker compose up --build -d
```

**Note**: Ports are configurable via the `FASTAPI_PORT` and `MLFLOW_UI_PORT` environment variables in your `.env` file.

### Using Docker

```bash
docker build -t cat-dog-classifier .
docker run -d -p 8000:8000 -p 5000:5000 \
  -e ENVIRONMENT=production \
  cat-dog-classifier
```

### Production Considerations

- Use a reverse proxy (nginx, Traefik) for HTTPS
- Set up proper CORS origins in `main.py`
- Use environment variables for sensitive configuration
- Consider using a production-grade database for MLflow
- Set up monitoring and logging
- Use a process manager (systemd, supervisor) for non-Docker deployments

## 🧪 Testing

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Test classification
curl -X POST "http://localhost:8000/api" \
  -F "file=@test_image.jpg"
```

## 🐛 Troubleshooting

### Model Not Loading

- Ensure `cats_dogs_finetuned_FT.keras` exists in the root directory
- Check file permissions
- Verify TensorFlow version compatibility

### Port Already in Use

```bash
# Find process using a specific port (e.g., 8888)
lsof -i :8888

# Kill the process or change port in .env file
# Update FASTAPI_PORT or MLFLOW_UI_PORT in .env and restart
```

### Docker Issues

```bash
# Clean up Docker resources
docker compose down -v
docker system prune -a

# Rebuild from scratch
docker compose build --no-cache
```

### MLflow Not Starting

- Check if the port specified in `MLFLOW_UI_PORT` (default: 5555) is available
- Verify SQLite database permissions
- Check Docker logs: `docker compose logs`
- Ensure `.env` file has `MLFLOW_UI_PORT` configured

## 📝 Dependencies

- **FastAPI**: Modern web framework for building APIs
- **TensorFlow**: Machine learning framework
- **MLflow**: ML lifecycle management and tracking

See `requirements.txt` for complete list.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👤 Authors

- **Boren Mon** - Developer ([Portfolio](https://borenmon.dev) | [GitHub](https://github.com/BorenMon))
- **AI Assistant (Claude)** - Development partner and code collaborator

## 🙏 Acknowledgments

- **Model Creator**: [wafaaelhusseini](https://www.kaggle.com/wafaaelhusseini) for providing the pre-trained [Cats vs Dogs Classifier model](https://www.kaggle.com/models/wafaaelhusseini/cats-vs-dogs-classifier) on Kaggle
- **Development**: Built collaboratively by Boren Mon and AI Assistant (Claude)
- TensorFlow team for the ML framework
- FastAPI for the excellent web framework
- MLflow for experiment tracking

## 📞 Support

For issues and questions:
- Open an issue on GitHub
