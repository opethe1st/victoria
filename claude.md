# Fitness Activity Tracker - Webapp Specification

## Overview
A web application that allows users to upload and analyze fitness activity data (.fit files) with automatic personal best (PB) tracking and activity time visualization.

## Core Features

### 1. Activity Data Management
- **File Upload**: Support for .fit file uploads (Garmin/Strava format)
- **Activity Types**: Swimming, Cycling, Running
- **Data Storage**: Local database (SQLite for simplicity)
- **Activity List**: View all uploaded activities with basic details (date, type, duration, distance)

### 2. Personal Best (PB) Tracking

**Swimming Standard Distances:**
- 100m, 200m, 400m, 750m, 1500m, 1900m, 3800m
- Track best continuous interval times within any activity

**Cycling Standard Distances:**
- 400m, 1km, 5km, 10km, 20km, 40km, 100km
- Track best continuous interval times

**Running Standard Distances:**
- 5km, 10km, 10 miles (16.09km), Half Marathon (21.1km), Marathon (42.2km)
- Track best continuous interval times

**PB Display:**
- Show current PB for each distance
- Show date achieved
- Historical PB progression

### 3. Activity Time Tracking & Visualization
- **Time aggregation by activity type:**
  - Daily view
  - Weekly view
  - Monthly view
- **Visualizations:**
  - Bar charts showing time spent per activity type
  - Line graphs showing trends over time
  - Stacked charts for comparing activity types

## Technical Stack

**Backend:**
- Python with Flask
- SQLite database
- fitparse library for parsing .fit files

**Frontend:**
- HTML/CSS/JavaScript
- Chart.js for visualizations
- Tailwind CSS for styling

**Architecture:**
- Multi-page application with Flask routing
- RESTful API for data operations
- Local file storage for uploaded .fit files

## Key Pages/Views

1. **Dashboard/Home**
   - Summary statistics
   - Recent activities
   - Quick PB overview

2. **Upload Page**
   - Drag-and-drop or file picker for .fit files
   - Upload progress
   - Success/error feedback

3. **Activities List**
   - Sortable/filterable table of all activities
   - Basic details: date, type, distance, duration, pace/speed

4. **Personal Bests Page**
   - Tabs or sections for each activity type
   - Table showing all standard distances with current PBs
   - Link to the activity where PB was achieved

5. **Analytics/Trends Page**
   - Time-based charts
   - Activity type breakdown
   - Selectable date ranges

## Database Schema

### Activities Table
- id (INTEGER PRIMARY KEY)
- activity_type (TEXT: 'swimming', 'cycling', 'running')
- upload_date (TIMESTAMP)
- activity_date (TIMESTAMP)
- duration (INTEGER - seconds)
- total_distance (REAL - meters)
- avg_heart_rate (INTEGER - optional)
- file_path (TEXT)

### GPS Points Table
- id (INTEGER PRIMARY KEY)
- activity_id (INTEGER FOREIGN KEY)
- timestamp (TIMESTAMP)
- latitude (REAL)
- longitude (REAL)
- distance (REAL - cumulative meters)
- speed (REAL - m/s)
- heart_rate (INTEGER - optional)

### Personal Bests Table
- id (INTEGER PRIMARY KEY)
- activity_type (TEXT)
- distance (REAL - meters)
- best_time (INTEGER - seconds)
- avg_pace (REAL - min/km or min/100m for swimming)
- activity_id (INTEGER FOREIGN KEY)
- achieved_date (TIMESTAMP)

### Time Aggregations Table
- id (INTEGER PRIMARY KEY)
- activity_type (TEXT)
- date (DATE)
- duration (INTEGER - seconds)
- aggregation_type (TEXT: 'daily', 'weekly', 'monthly')

## Processing Logic

### File Upload & Parsing
1. Parse .fit file to extract GPS points, timestamps, heart rate, etc.
2. Store raw data in database
3. Calculate total distance, duration, average pace

### PB Calculation
1. For each activity, analyze all continuous intervals matching standard distances
2. Compare against existing PBs
3. Update PB records if new records found
4. Use rolling window algorithm for efficiency

### Time Aggregation
1. Calculate daily totals on activity upload
2. Aggregate to weekly/monthly views on-demand or via scheduled process

## Implementation Phases

### Phase 1: Basic Infrastructure
- [ ] Project setup
- [ ] Database schema and models
- [ ] Basic Flask app structure
- [ ] File upload endpoint

### Phase 2: Activity Management
- [ ] .fit file parsing
- [ ] Activity storage
- [ ] Activity list view

### Phase 3: Personal Bests
- [ ] PB calculation algorithm
- [ ] PB storage
- [ ] PB display page

### Phase 4: Analytics & Visualization
- [ ] Time aggregation
- [ ] Chart implementation
- [ ] Analytics page

### Phase 5: UI/UX Polish
- [ ] Responsive design
- [ ] Error handling
- [ ] User feedback
