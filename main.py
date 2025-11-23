from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from io import BytesIO
import mlflow
from datetime import datetime
import uuid
import tempfile

# Load the model once at startup
MODEL_PATH = "cats_dogs_finetuned_FT.keras"
model = None
MLFLOW_EXPERIMENT_NAME = "cat_dog_classifier"

# MLflow configuration
mlflow.set_tracking_uri("sqlite:///mlflow.db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    global model
    try:
        # Setup MLflow experiment
        try:
            experiment = mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
            if experiment is None:
                mlflow.create_experiment(MLFLOW_EXPERIMENT_NAME)
                print(f"Created MLflow experiment: {MLFLOW_EXPERIMENT_NAME}")
            else:
                print(f"Using existing MLflow experiment: {MLFLOW_EXPERIMENT_NAME}")
        except Exception as e:
            print(f"Warning: Could not setup MLflow experiment: {str(e)}")
        
        # Load model
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH)
            print(f"Model loaded successfully from {MODEL_PATH}")
        else:
            print(f"Warning: Model file {MODEL_PATH} not found")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
    
    yield
    
    # Shutdown (if needed, add cleanup code here)
    pass

app = FastAPI(
    title="Cat or Dog Classifier API",
    description="""
    ⭐ The API accepts image uploads and returns classifications with confidence scores.
    ⭐ All classifications are logged to MLflow for tracking and analysis.
    """,
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "tryItOutEnabled": True,
    }
)

# Customize OpenAPI schema to add external documentation link
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add external documentation link
    openapi_schema["externalDocs"] = {
        "description": "Interactive Web UI",
        "url": "/",
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_image(image: Image.Image, target_size=(224, 224)) -> np.ndarray:
    """Preprocess image for model classification"""
    # Resize image
    image = image.resize(target_size)
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    # Convert to array and normalize
    img_array = np.array(image) / 255.0
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/api")
async def classify_image(file: UploadFile = File(...)):
    """
    Classify if an uploaded image is a cat or dog.
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON response with classification (cat or dog) and confidence score
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check if the model file exists.")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Classify image
        classification_result = model.predict(processed_image, verbose=0)
        
        # Assuming binary classification: [cat_probability, dog_probability]
        # Or single output: 0 = cat, 1 = dog (or vice versa)
        # We'll handle both cases
        if classification_result.shape[1] == 2:
            # Binary classification with 2 outputs
            cat_prob = float(classification_result[0][0])
            dog_prob = float(classification_result[0][1])
            classified_class = "dog" if dog_prob > cat_prob else "cat"
            confidence = float(max(cat_prob, dog_prob))
        else:
            # Single output (binary)
            prob = float(classification_result[0][0])
            # Assuming 0 = cat, 1 = dog (common convention)
            # If model outputs probability of dog, prob > 0.5 = dog
            classified_class = "dog" if prob > 0.5 else "cat"
            confidence = float(prob if prob > 0.5 else 1 - prob)
        
        # Calculate probabilities for response
        cat_probability = round(1 - confidence if classified_class == "dog" else confidence, 4)
        dog_probability = round(confidence if classified_class == "dog" else 1 - confidence, 4)
        
        # Log to MLflow
        try:
            mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
            with mlflow.start_run(run_name=f"classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"):
                # Log metrics
                mlflow.log_metric("confidence", confidence)
                mlflow.log_metric("cat_probability", cat_probability)
                mlflow.log_metric("dog_probability", dog_probability)
                
                # Log parameters
                mlflow.log_param("classified_class", classified_class)
                mlflow.log_param("model_path", MODEL_PATH)
                mlflow.log_param("image_format", file.content_type)
                mlflow.log_param("filename", file.filename or "unknown")
                
                # Log the image as an artifact
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                    image_path = tmp_file.name
                    image.save(image_path, "JPEG")
                    mlflow.log_artifact(image_path, "input_images")
                    os.remove(image_path)  # Clean up temp file
                
                # Log timestamp
                mlflow.log_param("timestamp", datetime.now().isoformat())
        except Exception as mlflow_error:
            # Don't fail the request if MLflow logging fails
            print(f"Warning: MLflow logging failed: {str(mlflow_error)}")
        
        return JSONResponse(content={
            "classification": classified_class,
            "confidence": round(confidence, 4),
            "probabilities": {
                "cat": cat_probability,
                "dog": dog_probability
            }
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/health", include_in_schema=False)
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

# Mount static files for UI
app.mount("", StaticFiles(directory="ui", html=True), name="ui")
