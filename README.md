# SlideForge - Paper-to-PPTX Converter

Convert research papers into professional PowerPoint presentations with AI-powered summarization and automatic slide generation.

## Features

- **PDF Processing**: Upload PDF files or provide DOI/URL for automatic paper retrieval
- **Smart Summarization**: AI-powered text summarization using TextRank or Hugging Face transformers
- **Section Detection**: Automatic detection of academic paper sections (Abstract, Introduction, Methods, etc.)
- **Professional Themes**: Three presentation themes (Academic, Minimal, Corporate)
- **Flexible Output**: Customizable bullet points per section (1-10 bullets, max 20 words each)
- **Multiple Interfaces**: Web UI and CLI for different use cases
- **Robust Architecture**: FastAPI backend with Next.js frontend

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SlideForge-Paper-To-PPTX-Converter
   ```

2. **Start with Docker Compose**:
   ```bash
   docker-compose -f docker/compose.yaml up --build
   ```

3. **Access the application**:
   - Web UI: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Set up environment**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the backend**:
   ```bash
   poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Run the frontend**:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

#### CLI Setup

1. **Navigate to CLI directory**:
   ```bash
   cd cli
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Use the CLI**:
   ```bash
   poetry run slideforge generate --pdf path/to/paper.pdf --theme academic --out presentation.pptx
   ```

## Usage

### Web Interface

1. Open http://localhost:3000 in your browser
2. Choose your input method:
   - **Upload PDF**: Drag and drop or browse for a PDF file
   - **DOI**: Enter a DOI identifier (e.g., 10.1038/nature12373)
   - **URL**: Provide a direct link to the paper
3. Select presentation theme and bullet count
4. Click "Generate Presentation"
5. Download your PowerPoint file

### CLI Usage

```bash
# Generate from PDF
slideforge generate --pdf paper.pdf --theme academic --max-bullets 6 --out presentation.pptx

# Generate from DOI
slideforge generate --doi 10.1038/nature12373 --theme minimal --max-bullets 4

# Generate from URL
slideforge generate --url https://example.com/paper.pdf --theme corporate --max-bullets 8

# Show information
slideforge info
```

### API Usage

```bash
# Generate presentation from PDF
curl -X POST "http://localhost:8000/v1/generate" \
  -H "Content-Type: multipart/form-data" \
  -F "pdf_file=@paper.pdf" \
  -F "theme=academic" \
  -F "max_bullets=6"

# Download generated presentation
curl -O "http://localhost:8000/v1/download/{file_id}"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SUMMARIZER_BACKEND` | Summarization method (`textrank`, `hf_transformer`) | `textrank` |
| `HF_MODEL_NAME` | Hugging Face model for summarization | `sshleifer/distilbart-cnn-12-6` |
| `UPLOAD_DIR` | Directory for uploaded files | `./uploads` |
| `OUTPUT_DIR` | Directory for generated files | `./outputs` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Themes

- **Academic**: Serif fonts, formal styling, suitable for academic presentations
- **Minimal**: Clean design, sans-serif fonts, generous white space
- **Corporate**: Professional styling with header/footer bands

## Development

### Running Tests

```bash
# Backend tests
cd backend
poetry run pytest

# With coverage
poetry run pytest --cov=app --cov-report=html
```

### Code Quality

```bash
# Format code
poetry run black app/
poetry run ruff check app/

# Run pre-commit hooks
poetry run pre-commit run --all-files
```

### Project Structure

```
SlideForge-Paper-To-PPTX-Converter/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration and logging
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── extractor/      # PDF text extraction
│   │   │   ├── sectionizer/    # Section detection
│   │   │   ├── summarizer/     # Text summarization
│   │   │   └── ppt/           # PowerPoint generation
│   │   ├── utils/         # Utility functions
│   │   └── tests/         # Test suite
│   ├── pyproject.toml     # Poetry configuration
│   └── README.md          # Backend documentation
├── frontend/              # Next.js frontend
│   ├── app/
│   │   ├── components/    # React components
│   │   ├── lib/          # Utilities and API client
│   │   └── page.tsx      # Main page
│   ├── package.json      # Node.js dependencies
│   └── tailwind.config.ts # Tailwind CSS configuration
├── cli/                   # Command-line interface
│   ├── paperslide/       # CLI implementation
│   └── pyproject.toml    # CLI dependencies
├── docker/               # Docker configuration
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── compose.yaml
└── README.md             # This file
```

## API Reference

### Endpoints

- `POST /v1/generate` - Generate PowerPoint from PDF/DOI/URL
- `GET /v1/download/{file_id}` - Download generated presentation

### Request Format

```json
{
  "pdf_file": "file", // Optional: PDF file upload
  "doi": "string",     // Optional: DOI identifier
  "url": "string",     // Optional: Paper URL
  "theme": "string",   // Required: academic, minimal, or corporate
  "max_bullets": 6     // Required: 1-10
}
```

### Response Format

```json
{
  "pptx_path": "string",
  "slide_count": 8,
  "metadata": {
    "title": "string",
    "authors": ["string"],
    "venue": "string",
    "year": 2023,
    "doi": "string",
    "url": "string"
  },
  "file_id": "string"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF text extraction
- [python-pptx](https://python-pptx.readthedocs.io/) for PowerPoint generation
- [sumy](https://github.com/miso-belica/sumy) for TextRank summarization
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
