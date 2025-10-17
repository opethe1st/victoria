# API Documentation

The application now includes a versioned REST API for programmatic access to fitness data.

## Base URL

```
http://127.0.0.1:5000/api/v1
```

## Endpoints

### Activities

#### Get All Activities
```
GET /api/v1/activities
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "activity_type": "running",
      "activity_date": "2025-10-17 10:00:00",
      "duration": 3600,
      "total_distance": 10000.0,
      "avg_heart_rate": 150
    }
  ],
  "count": 1
}
```

#### Get Activity by ID
```
GET /api/v1/activities/<activity_id>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "activity_type": "running",
    "activity_date": "2025-10-17 10:00:00",
    "duration": 3600,
    "total_distance": 10000.0,
    "avg_heart_rate": 150
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "Activity not found"
}
```

### Personal Bests

#### Get All Personal Bests
```
GET /api/v1/personal-bests
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "activity_type": "running",
      "distance": 5000.0,
      "best_time": 1200,
      "avg_pace": 4.0,
      "activity_id": 1,
      "achieved_date": "2025-10-17 10:00:00"
    }
  ],
  "count": 1
}
```

#### Get Personal Bests by Activity Type
```
GET /api/v1/personal-bests/<activity_type>
```

**Valid activity types:** `swimming`, `cycling`, `running`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "activity_type": "running",
      "distance": 5000.0,
      "best_time": 1200,
      "avg_pace": 4.0,
      "activity_id": 1,
      "achieved_date": "2025-10-17 10:00:00"
    }
  ],
  "count": 1
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid activity type. Must be one of: swimming, cycling, running"
}
```

## Response Format

All API responses follow this structure:

**Success:**
```json
{
  "success": true,
  "data": <response_data>,
  "count": <number_of_items>
}
```

**Error:**
```json
{
  "success": false,
  "error": "<error_message>"
}
```

## Example Usage

### Using cURL

```bash
# Get all activities
curl http://127.0.0.1:5000/api/v1/activities

# Get activity by ID
curl http://127.0.0.1:5000/api/v1/activities/1

# Get all personal bests
curl http://127.0.0.1:5000/api/v1/personal-bests

# Get running personal bests
curl http://127.0.0.1:5000/api/v1/personal-bests/running
```

### Using Python

```python
import requests

base_url = "http://127.0.0.1:5000/api/v1"

# Get all activities
response = requests.get(f"{base_url}/activities")
data = response.json()
print(f"Found {data['count']} activities")

# Get personal bests for running
response = requests.get(f"{base_url}/personal-bests/running")
data = response.json()
for pb in data['data']:
    print(f"{pb['distance']}m: {pb['best_time']}s")
```

## Future API Endpoints (Planned)

- `POST /api/v1/activities` - Upload new activity
- `DELETE /api/v1/activities/<id>` - Delete activity
- `GET /api/v1/analytics/time-aggregation` - Get time aggregation data
- `GET /api/v1/activities/<id>/gps-points` - Get GPS data for activity
