# API Documentation

The backend is built using FastAPI.

## POST /upload
Uploads a research paper in PDF format.

Request:
- File: PDF document

Response:
- Status message

## POST /query
Processes user questions.

Request:
- JSON with user query

Response:
- Answer text
- Citation metadata (paper title, authors, year)
