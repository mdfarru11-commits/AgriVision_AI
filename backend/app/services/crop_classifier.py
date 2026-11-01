import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageOps


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "models" / "plant_disease_dinov2"

MODEL_PATH = MODEL_DIR / "model.onnx"
CONFIG_PATH = MODEL_DIR / "config.json"


class CropClassifier:

    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            config = json.load(file)

        self.labels = {
            int(key): value
            for key, value in config["id2label"].items()
        }

        available = ort.get_available_providers()

        providers = []

        if "CoreMLExecutionProvider" in available:
            providers.append("CoreMLExecutionProvider")

        providers.append("CPUExecutionProvider")

        self.session = ort.InferenceSession(
            str(MODEL_PATH),
            providers=providers,
        )

        self.input_name = self.session.get_inputs()[0].name

        self.mean = np.array(
            [0.485, 0.456, 0.406],
            dtype=np.float32,
        ).reshape(1, 3, 1, 1)

        self.std = np.array(
            [0.229, 0.224, 0.225],
            dtype=np.float32,
        ).reshape(1, 3, 1, 1)

        print("Crop disease model loaded successfully.")
        print("Active providers:", self.session.get_providers())

    def preprocess(self, image: Image.Image) -> np.ndarray:

        image = ImageOps.exif_transpose(image).convert("RGB")

        width, height = image.size

        scale = 256 / min(width, height)

        new_width = round(width * scale)
        new_height = round(height * scale)

        image = image.resize(
            (new_width, new_height),
            Image.Resampling.BICUBIC,
        )

        left = (new_width - 224) // 2
        top = (new_height - 224) // 2

        image = image.crop(
            (left, top, left + 224, top + 224)
        )

        pixels = np.asarray(image, dtype=np.float32) / 255.0

        pixels = np.transpose(pixels, (2, 0, 1))
        pixels = np.expand_dims(pixels, axis=0)

        pixels = (pixels - self.mean) / self.std

        return np.ascontiguousarray(pixels, dtype=np.float32)

    def predict(self, image: Image.Image) -> dict:

        input_tensor = self.preprocess(image)

        outputs = self.session.run(
            ["logits"],
            {self.input_name: input_tensor},
        )

        logits = outputs[0][0]

        shifted = logits - np.max(logits)
        probabilities = np.exp(shifted)
        probabilities = probabilities / np.sum(probabilities)

        top_indices = np.argsort(probabilities)[::-1][:3]

        predictions = []

        for index in top_indices:

            label = self.labels[int(index)]

            if "___" in label:
                crop, condition = label.split("___", 1)
            else:
                crop = "Unknown"
                condition = label

            predictions.append({
                "crop": crop,
                "condition": condition,
                "label": label,
                "confidence": round(
                    float(probabilities[index]) * 100,
                    2,
                ),
            })

        return {
            "predicted_class": predictions[0]["label"],
            "confidence": predictions[0]["confidence"],
            "predictions": predictions,
            "model": "Plant Disease DINOv2 Small",
            "notice": (
                "Predictions are model estimates, not confirmed "
                "diagnoses. Field conditions may differ from "
                "training images."
            ),
        }


classifier = CropClassifier()
