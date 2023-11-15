# metrics-backend

We need a Frontend + Backend application that allows you to post and visualize metrics. Each metric will have: Timestamp, name, and value. The metrics will be shown in a timeline and must show averages per minute/hour/day. The metrics will be persisted in the database.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

Make sure you have the following installed:

- Python 3.10
- `pipenv`

### Installing

Clone the repository:

```bash
git clone https://github.com/viktorsalanki/metrics-backend.git
cd metrics-backend
```

Create a virtual environment and install dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```
> **__Note:__** you might need to reopen your terminal


### Database Setup

Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Running the application

```bash
python manage.py runserver
```
Visit http://localhost:8000/api/v1/metrics/ in your browser.


## Usage

The app provides a RESTful API for posting and retrieving metrics data. Follow the instructions below to interact with the API.

### API Endpoints

- **GET `/api/v1/metrics/`**: Retrieve a list of all metrics.
- **GET `/api/v1/metrics/{id}/`**: Retrieve details of a specific metric.
- **POST `/api/v1/metrics/`**: Add a new metric.
- **PUT `/api/v1/metrics/{id}/`**: Update details of a specific metric.
- **DELETE `/api/v1/metrics/{id}/`**: Delete a specific metric.
- **GET `/api/v1/stats/averages/?interval=<minute|hour|day>`**: Get average metric values based on a specified interval.

### Sample HTTP Requests

### Get all metrics

```bash
curl http://localhost:8000/api/v1/metrics/
```

### Get a specific metric

```bash
curl http://localhost:8000/api/v1/metrics/2/
```

### Add a new metric

```bash
curl -X POST -H "Content-Type: application/json" -d '{"timestamp": "2023-11-10T12:00:00Z", "name": "example_metric", "value": 42.0}' http://localhost:8000/api/v1/metrics/
```
> **__Note:__** timestamp can be any valid ISO 8601 format, currently supports only UTC timezone.

### Get average per hour

```bash
curl http://localhost:8000/api/v1/stats/averages/?interval=hour
```
