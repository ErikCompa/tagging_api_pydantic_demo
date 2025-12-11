# fastAPI routes for tagging API

from fastapi import FastAPI, HTTPException
from app.models import (ArtifactResponse, ArtifactType, SpeechAnalysisRequest, ImageAnalysisRequest, Artifact, TagSummaryResponse)
from app.tagging import tag_speech, tag_image
from app.storage import create_artifact, get_artifact_by_id, list_artifacts, summarize_tags
from app.google_vision import get_image_labels

app = FastAPI(title="Tagging API", description="API for tagging speech and images", version="1.0.0")

@app.post(
    '/speech/analyze',
    response_model=Artifact,
    summary="Analyze speech transcript and generate tags",
)
async def analyze_speech(payload: SpeechAnalysisRequest):
    tags = tag_speech(payload.transcript)

    artifact = create_artifact(
        type_=ArtifactType.SPEECH,
        language=payload.language,
        tags=tags,
    )

    return artifact

@app.post(
    '/image/analyze',
    response_model=Artifact,
    tags=["images"],
    summary="Analyze image URL and generate tags",
)
async def analyze_image(payload: ImageAnalysisRequest):
    try:
        labels = await get_image_labels(str(payload.image_url))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching image labels from Google Vision API: {e}")
    
    tags = tag_image(labels)

    artifact = create_artifact(
        type_=ArtifactType.IMAGE,
        language=payload.language,
        tags=tags,
    )

    return artifact

@app.get(
    '/artifacts',
    response_model=ArtifactResponse,
    summary="List all analyzed artifacts",
)
async def get_artifacts():
    return ArtifactResponse(items=list_artifacts())

@app.get(
    '/artifacts/{artifact_id}',
    response_model=Artifact,
    tags=["artifacts"],
    summary="Get artifact by ID",
)
async def get_artifact(artifact_id: str):
    artifact = get_artifact_by_id(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return artifact

@app.get(
    '/tags',
    response_model=TagSummaryResponse,
    tags=["tags"],
    summary="Get summary of tags across all artifacts",
)
async def get_tag_summary():
    return summarize_tags()
