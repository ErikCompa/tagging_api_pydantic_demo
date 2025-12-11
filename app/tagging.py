# tagging logic for speech and google vision labels

from typing import List, Set, Dict
from app.models import Tag, TagCategory

ANIMALS: Set[str] = {"cat", "dog", "bird", "fish", "lion", "tiger"}
LOCATIONS: Set[str] = {"beach", "mountain", "city", "forest", "desert", "river", "park"}
COLORS: Set[str] = {"red", "blue", "green", "yellow", "black", "white", "orange", "purple"}
GENRES: Set[str] = {"jazz", "rock", "pop", "classical", "hip hop", "country"}
TOPICS: Set[str] = {"sports", "politics", "technology", "health", "music", "travel"}
TIMES_OF_DAY: Set[str] = {"morning", "afternoon", "evening", "night"}

def tag_speech(transcript: str) -> List[Tag]:
    
    # simple keyword-based tagging for speech transcripts

    # normalize transcript to lowercase
    text_lower = transcript.lower()
    tags: List[Tag] = []

    # helper to add tags if keywords found
    def add_if_found(keywords: Set[str], category: TagCategory) -> None:
        for keyword in keywords:
            if keyword in text_lower:
                tags.append(Tag(category=category, value=keyword))

    add_if_found(ANIMALS, TagCategory.ANIMAL)
    add_if_found(LOCATIONS, TagCategory.LOCATION)
    add_if_found(COLORS, TagCategory.COLOR)
    add_if_found(GENRES, TagCategory.GENRE)
    add_if_found(TOPICS, TagCategory.TOPIC)
    add_if_found(TIMES_OF_DAY, TagCategory.TIME_OF_DAY)

    # remove duplicates
    unique: Dict[tuple[str, str], Tag] = {}
    for tag in tags:
        unique[(tag.category.value, tag.value)] = tag
    return list(unique.values())

def tag_image(labels: List[str]) -> List[Tag]:
    
    # simple keyword-based tagging for image labels

    tags: List[Tag] = []

    for label in labels:
        label_lower = label.lower()

        if label_lower in ANIMALS:
            cat = TagCategory.ANIMAL

        elif label_lower in LOCATIONS:
            cat = TagCategory.LOCATION

        elif label_lower in COLORS:
            cat = TagCategory.COLOR

        elif label_lower in GENRES:
            cat = TagCategory.GENRE

        elif label_lower in TOPICS:
            cat = TagCategory.TOPIC

        elif label_lower in TIMES_OF_DAY:
            cat = TagCategory.TIME_OF_DAY

        else:
            cat = TagCategory.OTHER

        tags.append(Tag(category=cat, value=label))

    # remove duplicates
    unique: Dict[tuple[str, str], Tag] = {}
    for tag in tags:
        unique[(tag.category.value, tag.value)] = tag
    return list(unique.values())
