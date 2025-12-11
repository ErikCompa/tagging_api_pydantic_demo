# mock db

from datetime import datetime, timezone
from typing import List, Dict, Optional
from uuid import uuid4
from app.models import Artifact, ArtifactType, Tag, TagCategory, TagSummary, TagSummaryResponse

# mock in-memory db
ARTIFACTS_DB: List[Artifact] = []

def create_artifact(type_: ArtifactType, language: str, tags: List[Tag]) -> Artifact:
    
    # create new artifact and store in mock db

    artifact = Artifact(
        id=str(uuid4()),
        type=type_,
        language=language,
        tags=tags,
        created_at=datetime.now(timezone.utc)
    )

    ARTIFACTS_DB.append(artifact)
    return artifact

def get_artifact_by_id(artifact_id: str) -> Optional[Artifact]:
    
    # retrieve artifact by id from mock db
    
    for artifact in ARTIFACTS_DB:
        if artifact.id == artifact_id:
            return artifact
    return None

def list_artifacts() -> List[Artifact]:
    
    # list all artifacts in mock db
    
    return ARTIFACTS_DB

def summarize_tags() -> TagSummaryResponse:
    
    # summarize tags and their counts across all artifacts in mock db
    
    counter: Dict[tuple[str, str], int] = {}

    for artifact in ARTIFACTS_DB:
        for tag in artifact.tags:
            key = (tag.category.value, tag.value)
            counter[key] = counter.get(key, 0) + 1

    summaries: List[TagSummary] = []
    for (cat_val, tag_val), count in counter.items():
        summaries.append(
            TagSummary(
                value=tag_val,
                category=cat_val,
                count=count
            )
        )
    
    return TagSummaryResponse(items=summaries)
