# Tagging API

A FastAPI-based API for analyzing and tagging speech transcripts and images. Uses keyword matching for speech transcripts and Google Vision API for image label detection.

## Features

- Analyze speech transcripts and generate tags based on keywords
- Analyze images via URL using Google Vision API for label detection
- Categorize tags into predefined categories (animal, location, color, genre, topic, time of day)
- Store analyzed artifacts with unique IDs
- Retrieve individual artifacts or list all artifacts
- Get tag summaries with counts across all artifacts

## Prerequisites

- Python 3.8+
- Google Cloud Vision API key

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_api_key_here
```

## Running the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Access the interactive API documentation at `http://localhost:8000/docs`

## Testing

### Test Speech Analysis

Use this JSON payload to test the speech analysis endpoint:

```json
{
  "type": "speech",
  "transcript": "I saw a dog at the beach this morning",
  "language": "en"
}
```

### Test Image Analysis

Use this JSON payload to test the image analysis endpoint with Google Vision API:

```json
{
  "type": "image",
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
  "language": "en"
}
```

## API Endpoints

### POST /speech/analyze

Analyze a speech transcript and generate tags.

**Request Body:**
```json
{
  "type": "speech",
  "transcript": "I saw a dog at the beach this morning",
  "language": "en"
}
```

**Response:**
```json
{
  "id": "uuid",
  "type": "speech",
  "language": "en",
  "tags": [
    {"category": "animal", "value": "dog"},
    {"category": "location", "value": "beach"},
    {"category": "time_of_day", "value": "morning"}
  ],
  "created_at": "2025-12-10T12:34:56.789Z"
}
```

### POST /image/analyze

Analyze an image URL and generate tags using Google Vision API.

**Request Body:**
```json
{
  "type": "image",
  "image_url": "https://example.com/image.jpg",
  "language": "en"
}
```

**Response:**
```json
{
  "id": "uuid",
  "type": "image",
  "language": "en",
  "tags": [
    {"category": "animal", "value": "cat"},
    {"category": "color", "value": "blue"}
  ],
  "created_at": "2025-12-10T12:34:56.789Z"
}
```

### GET /artifacts

List all analyzed artifacts.

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "type": "speech",
      "language": "en",
      "tags": [...],
      "created_at": "2025-12-10T12:34:56.789Z"
    }
  ]
}
```

### GET /artifacts/{artifact_id}

Get a specific artifact by ID.

**Response:**
```json
{
  "id": "uuid",
  "type": "image",
  "language": "en",
  "tags": [...],
  "created_at": "2025-12-10T12:34:56.789Z"
}
```

### GET /tags

Get summary of all tags with their counts across all artifacts.

**Response:**
```json
{
  "items": [
    {
      "value": "dog",
      "category": "animal",
      "count": 5
    },
    {
      "value": "beach",
      "category": "location",
      "count": 3
    }
  ]
}
```

## Project Structure

```
tagging_api/
├── app/
│   ├── __init__.py
│   ├── config.py          # Environment configuration
│   ├── google_vision.py   # Google Vision API integration
│   ├── main.py            # FastAPI routes
│   ├── models.py          # Pydantic models
│   ├── storage.py         # In-memory data storage
│   └── tagging.py         # Tagging logic
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md
```

## Tag Categories

- **animal**: Animals (cat, dog, bird, fish, lion, tiger)
- **location**: Places (beach, mountain, city, forest, desert, river, park)
- **color**: Colors (red, blue, green, yellow, black, white, orange, purple)
- **genre**: Music genres (jazz, rock, pop, classical, hip hop, country)
- **topic**: General topics (sports, politics, technology, health, music, travel)
- **time_of_day**: Time periods (morning, afternoon, evening, night)
- **other**: Uncategorized tags

## Notes

- This implementation uses in-memory storage for artifacts (data is lost on restart)
- Speech tagging uses simple keyword matching
- Image tagging relies on Google Vision API label detection
- All tag values are normalized to lowercase
- Duplicate tags within an artifact are automatically removed
