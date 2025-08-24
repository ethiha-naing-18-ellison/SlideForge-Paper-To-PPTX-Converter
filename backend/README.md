# SlideForge Backend

Paper-to-PPTX Converter Backend API

## Features

- PDF text extraction using PyMuPDF with fallback to pdfminer.six
- Academic section detection and parsing
- Text summarization using TextRank or Hugging Face transformers
- PowerPoint generation with customizable themes
- FastAPI REST API with async support
- Comprehensive test suite

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SlideForge-Paper-To-PPTX-Converter/backend
```

2. Install dependencies:
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

3. Set up environment:
```bash
cp env.example .env
# Edit .env with your configuration
```

### Running the Application

#### Development Server
```bash
# Using Poetry
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Server
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /v1/generate
Generate PowerPoint from PDF or DOI/URL

**Parameters:**
- `pdf_file`: PDF file upload (optional)
- `doi`: DOI identifier (optional)
- `url`: Paper URL (optional)
- `theme`: Presentation theme (academic, minimal, corporate)
- `max_bullets`: Maximum bullets per section (default: 6)

**Response:**
```json
{
  "pptx_path": "path/to/generated.pptx",
  "slide_count": 8,
  "metadata": {
    "title": "Paper Title",
    "authors": ["Author 1", "Author 2"],
    "venue": "Conference/Journal",
    "year": 2023
  }
}
```

### GET /v1/download/{file_id}
Download generated PowerPoint file

## Development

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest app/tests/test_extractor.py
```

### Code Quality
```bash
# Format code
poetry run black app/

# Lint code
poetry run ruff check app/

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

### Project Structure
```
app/
├── api/           # FastAPI routes
├── core/          # Configuration and logging
├── models/        # Pydantic schemas
├── services/      # Business logic
│   ├── extractor/     # PDF text extraction
│   ├── sectionizer/   # Section detection
│   ├── summarizer/    # Text summarization
│   └── ppt/          # PowerPoint generation
├── utils/         # Utility functions
└── tests/         # Test suite
```

## Configuration

Key environment variables:

- `SUMMARIZER_BACKEND`: Summarization method (textrank, hf_transformer)
- `HF_MODEL_NAME`: Hugging Face model for summarization
- `UPLOAD_DIR`: Directory for uploaded files
- `OUTPUT_DIR`: Directory for generated files
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details
