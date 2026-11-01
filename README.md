# AgriVision AI 🌱

### AI-Powered Crop Health Monitoring and Targeted Agricultural Intervention

**Team:** ByteSquad
**Team Leader:** Mohd Farman
**Problem Statement:** 9 — AI-Powered Crop Health Mapping and Targeted Agricultural Intervention

## Overview

AgriVision AI is an AI-powered crop health monitoring prototype designed to help identify potential crop diseases from leaf images.

The system uses a pretrained DINOv2-based image classification model exported to ONNX format. Users upload a crop image through a Streamlit interface, and a FastAPI backend processes the image and returns predicted crop conditions with confidence scores.

## Key Features

- Crop image upload and analysis.
- AI-powered crop disease classification.
- Top-three prediction results.
- Prediction confidence scores.
- Crop health dashboard.
- Illustrative field-zone visualization.
- General crop-care recommendations.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Model | DINOv2 Small |
| Model Runtime | ONNX Runtime |
| Image Processing | Pillow, NumPy |
| Programming Language | Python |

## System Architecture

1. User uploads a crop image.
2. Streamlit sends the image to the FastAPI backend.
3. FastAPI validates and preprocesses the image.
4. ONNX Runtime executes the pretrained classification model.
5. The backend returns the top predictions and confidence scores.
6. Streamlit displays the analysis results.

## Project Structure

```text
AgriVision_AI/
├── app.py
├── requirements.txt
├── README.md
├── alembic.ini
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── models/
│   │   └── plant_disease_dinov2/
│   └── alembic/
├── modules/
├── pages/
└── data/
```

## Running Locally

### Frontend

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

### Backend

```bash
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Backend API documentation:

`http://127.0.0.1:8000/docs`

## Current Prototype Limitations

- The classifier uses a pretrained model with 38 PlantVillage classes.
- Real-world field-image validation is still required.
- The field-zone visualization is illustrative and is not a real GPS-based crop-health map.
- Recommendations are general guidance, not confirmed diagnoses or pesticide prescriptions.
- Multispectral analysis and NDVI are not currently implemented.

## Future Scope

- Geotagged field imagery and actual spatial crop-health mapping.
- Validation using diverse field datasets.
- Multispectral image analysis.
- Improved crop-specific recommendations.
- Integration with agricultural monitoring devices and autonomous data-collection systems.

## Disclaimer

AI predictions are estimates and should not replace expert agricultural diagnosis. Always consult a qualified agricultural expert before taking crop-treatment decisions.

---

**AgriVision AI — Smarter Crop Monitoring, Better Agricultural Decisions.**