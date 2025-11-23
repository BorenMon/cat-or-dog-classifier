const API_URL = '/api';
let selectedFile = null;

// File input change handler
const fileInput = document.getElementById('fileInput');
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Browse button click handler
const browseBtn = document.getElementById('browseBtn');
browseBtn.addEventListener('click', function(e) {
    e.stopPropagation(); // Prevent event from bubbling to upload area
    fileInput.click();
});

// Drag and drop handlers
const uploadArea = document.getElementById('uploadArea');

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFileSelect(file);
    } else {
        showError('Please select a valid image file');
    }
});

// Click to upload (but not when clicking the button)
uploadArea.addEventListener('click', (e) => {
    // Don't trigger if clicking the button or its children
    if (e.target !== browseBtn && !browseBtn.contains(e.target)) {
        fileInput.click();
    }
});

function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }

    selectedFile = file;
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const previewImage = document.getElementById('previewImage');
        previewImage.src = e.target.result;
        
        // Show preview section, hide upload section
        document.getElementById('uploadSection').style.display = 'none';
        document.getElementById('previewSection').style.display = 'block';
        document.getElementById('resultSection').style.display = 'none';
        hideError();
    };
    
    reader.readAsDataURL(file);
}

async function classifyImage() {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }

    const classifyBtn = document.getElementById('classifyBtn');
    const btnText = classifyBtn.querySelector('.btn-text');
    const btnLoader = classifyBtn.querySelector('.btn-loader');
    
    // Show loading state
    classifyBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    hideError();

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to classify image');
        }

        const result = await response.json();
        displayResult(result);
    } catch (error) {
        showError(error.message || 'An error occurred while classifying the image');
    } finally {
        // Reset button state
        classifyBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function displayResult(result) {
    const { classification, confidence, probabilities } = result;
    
    // Update result icon and title
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    
    if (classification === 'cat') {
        resultIcon.textContent = '🐱';
        resultIcon.className = 'result-icon cat';
        resultTitle.textContent = 'It\'s a Cat!';
    } else {
        resultIcon.textContent = '🐶';
        resultIcon.className = 'result-icon dog';
        resultTitle.textContent = 'It\'s a Dog!';
    }
    
    // Update confidence
    const confidencePercent = (confidence * 100).toFixed(1);
    document.getElementById('confidenceValue').textContent = `${confidencePercent}%`;
    document.getElementById('confidenceFill').style.width = `${confidence * 100}%`;
    
    // Update probabilities
    document.getElementById('catProb').textContent = `${(probabilities.cat * 100).toFixed(1)}%`;
    document.getElementById('dogProb').textContent = `${(probabilities.dog * 100).toFixed(1)}%`;
    
    // Show result section
    document.getElementById('resultSection').style.display = 'block';
    
    // Animate result card
    setTimeout(() => {
        document.getElementById('resultCard').classList.add('show');
    }, 10);
}

function resetUpload() {
    selectedFile = null;
    fileInput.value = ''; // Reset file input to allow selecting the same file again
    document.getElementById('previewImage').src = '';
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('resultCard').classList.remove('show');
    hideError();
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}

