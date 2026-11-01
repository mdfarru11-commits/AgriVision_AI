import base64
import binascii
from io import BytesIO

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image, UnidentifiedImageError

from backend.app.services.crop_classifier import classifier

app = FastAPI(title="AgriVision AI", version="1.0.0")


class AnalyzeRequest(BaseModel):
    file_name: str
    image_base64: str


@app.get("/")
def root():
    return {"status": "running", "service": "AgriVision AI"}


@app.get("/health")
def health():
    return {"status": "healthy", "model": "loaded"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        raw = base64.b64decode(request.image_base64, validate=True)

        if len(raw) > 8 * 1024 * 1024:
            raise HTTPException(413, "Image must be smaller than 8 MB")

        image = Image.open(BytesIO(raw))
        image.verify()

        image = Image.open(BytesIO(raw)).convert("RGB")
        result = classifier.predict(image)

        return {
            "status": "success",
            "file_name": request.file_name,
            **result,
        }

    except HTTPException:
        raise
    except (binascii.Error, ValueError):
        raise HTTPException(400, "Invalid image encoding")
    except (UnidentifiedImageError, OSError):
        raise HTTPException(400, "Invalid image file")
