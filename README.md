# FastAPI Python Simulation Image

A FastAPI-based Python application for simulation and image processing.

## Project Structure

```
fastapi-py-sim-img/
│── app/
│   ├── __init__.py
│   └── main.py
│── requirements.txt
│── .gitignore
│── README.md
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Open your browser and navigate to:
   - API: http://localhost:8000
   - Interactive API docs (Swagger): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Development

The application uses FastAPI with automatic interactive API documentation. You can explore the API endpoints using the built-in Swagger UI at `/docs`.

## License

This project is open source and available under the [MIT License](LICENSE).