# google vision api call 
# https://docs.cloud.google.com/vision/docs/labels

from typing import List
import httpx
from app.config import GOOGLE_VISION_URL

async def get_image_labels(img_url: str) -> List[str]:
    payload = {
        "requests": [
            {
                "image": {"source": {"imageUri": img_url}},
                "features": [{"type": "LABEL_DETECTION", "maxResults": 10}],
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_VISION_URL, json=payload)
        response.raise_for_status()
        data = response.json()

    responses = data.get("responses", [])
    if not responses:
        return []
    
    label_annotations = responses[0].get("labelAnnotations", []) or []

    labels: list[str] = [
        annotation["description"] for annotation in label_annotations if "description" in annotation
    ]

    return labels
