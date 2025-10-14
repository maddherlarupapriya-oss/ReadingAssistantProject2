// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Remove active class from all
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active to clicked
        btn.classList.add('active');
        document.getElementById(tabName + '-tab').classList.add('active');
    });
});

// File Upload - Drag & Drop
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');

dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        uploadBtn.disabled = false;
        showAlert('File selected: ' + e.dataTransfer.files[0].name, 'success');
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
        uploadBtn.disabled = false;
        showAlert('File selected: ' + fileInput.files[0].name, 'success');
    }
});

// File Upload Submit
document.getElementById('fileUploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('source', 'file');
    
    try {
        showAlert('Uploading...', 'info');
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Upload successful! Redirecting to reader...', 'success');
            setTimeout(() => {
                window.location.href = `/reader/${data.doc_id}`;
            }, 1000);
        } else {
            showAlert(data.message || 'Upload failed', 'error');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'error');
        console.error('Upload error:', error);
    }
});

// Paste Text Submit
document.getElementById('pasteTextForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const text = document.getElementById('pasteTextArea').value.trim();
    
    if (!text) {
        showAlert('Please enter some text', 'error');
        return;
    }
    
    try {
        showAlert('Processing...', 'info');
        const response = await fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text, source: 'paste' })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Text processed! Redirecting to reader...', 'success');
            setTimeout(() => {
                window.location.href = `/reader/${data.doc_id}`;
            }, 1000);
        } else {
            showAlert(data.message || 'Processing failed', 'error');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'error');
        console.error('Paste error:', error);
    }
});

// Camera functionality
const cameraBtn = document.getElementById('cameraBtn');
const cameraSection = document.getElementById('cameraSection');
const cameraPreview = document.getElementById('cameraPreview');
const captureBtn = document.getElementById('captureBtn');
const retakeBtn = document.getElementById('retakeBtn');
const closeCameraBtn = document.getElementById('closeCameraBtn');
const capturedImagePreview = document.getElementById('capturedImagePreview');
const capturedImage = document.getElementById('capturedImage');
const processCaptureBtn = document.getElementById('processCaptureBtn');
const captureCanvas = document.getElementById('captureCanvas');

let cameraStream = null;

cameraBtn.addEventListener('click', async () => {
    fileSection.style.display = 'none';
    cameraSection.style.display = 'block';
    
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment',
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            } 
        });
        cameraPreview.srcObject = cameraStream;
        showStatus('Camera ready! Position your document and capture.', 'info');
    } catch (error) {
        showStatus('Camera access denied. Please allow camera access.', 'error');
        console.error('Camera error:', error);
        cameraSection.style.display = 'none';
        fileSection.style.display = 'block';
    }
});

closeCameraBtn.addEventListener('click', () => {
    stopCamera();
    cameraSection.style.display = 'none';
    fileSection.style.display = 'block';
    capturedImagePreview.style.display = 'none';
    showStatus('Camera closed', 'info');
});

captureBtn.addEventListener('click', () => {
    const context = captureCanvas.getContext('2d');
    captureCanvas.width = cameraPreview.videoWidth;
    captureCanvas.height = cameraPreview.videoHeight;
    context.drawImage(cameraPreview, 0, 0);
    
    const imageDataUrl = captureCanvas.toDataURL('image/jpeg', 0.9);
    capturedImage.src = imageDataUrl;
    
    capturedImagePreview.style.display = 'block';
    captureBtn.style.display = 'none';
    retakeBtn.style.display = 'inline-block';
    cameraPreview.style.display = 'none';
    
    stopCamera();
    
    showStatus('Photo captured! Click "Process This Image" to extract text.', 'success');
});

retakeBtn.addEventListener('click', async () => {
    capturedImagePreview.style.display = 'none';
    captureBtn.style.display = 'inline-block';
    retakeBtn.style.display = 'none';
    cameraPreview.style.display = 'block';
    
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                facingMode: 'environment',
                width: { ideal: 1920 },
                height: { ideal: 1080 }
            } 
        });
        cameraPreview.srcObject = cameraStream;
        showStatus('Camera ready! Take another photo.', 'info');
    } catch (error) {
        showStatus('Camera access denied.', 'error');
    }
});

processCaptureBtn.addEventListener('click', () => {
    captureCanvas.toBlob(async (blob) => {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        await uploadFile(file);
    }, 'image/jpeg', 0.9);
});

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
        cameraPreview.srcObject = null;
    }
}

// Stop camera when page is closed
window.addEventListener('beforeunload', stopCamera);

// Delete document
document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to delete this document?')) return;
        
        const docId = btn.dataset.docId;
        
        try {
            const response = await fetch(`/delete/${docId}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.success) {
                btn.closest('.document-card').remove();
                showAlert('Document deleted', 'success');
            } else {
                showAlert('Delete failed', 'error');
            }
        } catch (error) {
            showAlert('Network error', 'error');
        }
    });
});

// Alert function
function showAlert(message, type) {
    const alertBox = document.getElementById('alertBox');
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.classList.remove('hidden');
    
    setTimeout(() => {
        alertBox.classList.add('hidden');
    }, 4000);
}
