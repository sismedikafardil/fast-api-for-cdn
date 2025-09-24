# FastAPI S3 Bridge

A small FastAPI service that bridges the frontend to Amazon S3 object storage by
generating presigned upload URLs and public file URLs. Frontends can request a
presigned URL from this service, upload directly to S3, and then use the public
URL to reference the uploaded object.

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

- `POST /generate-presigned-url` - Generate a presigned PUT URL and public object URL

Example request to generate a presigned URL:

```bash
curl -s -X POST -H "Content-Type: application/json" \
   -d '{"filename":"uploads/test.png","content_type":"image/png"}' \
   http://127.0.0.1:8000/generate-presigned-url | jq .
```

The response contains `upload_url` (use with `PUT`) and `public_url`.

## Development

The application uses FastAPI with automatic interactive API documentation. You can explore the API endpoints using the built-in Swagger UI at `/docs`.

## License

This project is open source and available under the [MIT License](LICENSE).