# SlideForge - How to Run

This guide provides step-by-step instructions to run the SlideForge Paper-to-PPTX Converter.

## 🚀 Quick Start Options

Choose one of the following methods to run SlideForge:

1. **Backend Only** - FastAPI server with API endpoints
2. **Frontend Only** - Next.js web interface
3. **CLI Only** - Command-line interface
4. **Full Stack** - Backend + Frontend together
5. **Docker** - Containerized deployment

---

## 📋 Prerequisites

### Required Software
- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Poetry** - Python dependency manager
- **pnpm** - Node.js package manager (or npm)

### Install Poetry (if not installed)
```bash
# Windows
powershell -Command "(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -"

# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

### Install pnpm (if not installed)
```bash
npm install -g pnpm
```

---

## 🔧 Method 1: Backend Only (FastAPI)

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Install Dependencies
```bash
poetry install
```

### Step 3: Run the Server
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Access the API
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### API Endpoints Available
- `POST /v1/generate` - Upload PDF and generate PowerPoint
- `GET /v1/download/{file_id}` - Download generated PowerPoint

---

## 🌐 Method 2: Frontend Only (Next.js)

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
pnpm install
```

### Step 3: Run the Development Server
```bash
pnpm dev
```

### Step 4: Access the Web Interface
- **Web App**: http://localhost:3000

**Note**: Frontend requires backend to be running for full functionality.

---

## 💻 Method 3: CLI Only

### Step 1: Navigate to CLI Directory
```bash
cd cli
```

### Step 2: Install Dependencies
```bash
poetry install
```

### Step 3: Run CLI Commands

#### Generate PowerPoint from PDF
```bash
poetry run python -m paperslide.cli generate --pdf path/to/paper.pdf --theme academic --out output.pptx
```

#### Available Options
- `--pdf`: Path to input PDF file
- `--theme`: Choose from `academic`, `minimal`, `corporate`
- `--max-bullets`: Maximum bullets per section (default: 6)
- `--out`: Output PowerPoint file path

#### Example Commands
```bash
# Basic usage
poetry run python -m paperslide.cli generate --pdf research_paper.pdf --theme academic --out presentation.pptx

# With custom settings
poetry run python -m paperslide.cli generate --pdf paper.pdf --theme minimal --max-bullets 4 --out slides.pptx

# Corporate theme
poetry run python -m paperslide.cli generate --pdf document.pdf --theme corporate --out corporate_presentation.pptx
```

---

## 🖥️ Method 4: Full Stack (Backend + Frontend)

### Option A: Run in Separate Terminals

#### Terminal 1 - Backend
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
pnpm install
pnpm dev
```

### Option B: Run Backend First, Then Frontend
```bash
# Start backend
cd backend && poetry install && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In new terminal, start frontend
cd frontend && pnpm install && pnpm dev
```

### Access Points
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health

---

## 🐳 Method 5: Docker Deployment

### Prerequisites
- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
- **Docker Compose** (usually included with Docker Desktop)

### Step 1: Navigate to Project Root
```bash
cd SlideForge-Paper-To-PPTX-Converter
```

### Step 2: Build and Run with Docker Compose
```bash
docker-compose -f docker/compose.yaml up --build
```

### Step 3: Access the Application
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

### Stop Docker Services
```bash
docker-compose -f docker/compose.yaml down
```

---

## 🧪 Testing the Installation

### Test Backend
```bash
cd backend
poetry run pytest app/tests/ -v
```

### Test End-to-End Pipeline
```bash
cd backend
poetry run python test_end_to_end.py
```

### Expected Output
```
🚀 Testing SlideForge End-to-End Pipeline
==================================================
1. Extracting text from PDF...
   ✅ Extracted 2,708 characters

2. Splitting text into sections...
   ✅ Found 10 sections

3. Summarizing sections...
   ✅ abstract: 2 bullets
   ✅ methods: 2 bullets
   ...

4. Creating presentation metadata...
   ✅ Created metadata

5. Building PowerPoint presentation...
   ✅ Created presentation: test_output.pptx
   📊 Total slides: 11

==================================================
🎉 End-to-end test completed successfully!
```

---

## 🔧 Configuration

### Environment Variables (Optional)
Create `.env` file in the `backend` directory:

```env
# Backend Configuration
SUMMARIZER_BACKEND=textrank
HF_MODEL_NAME=sshleifer/distilbart-cnn-12-6
ENABLE_NETWORK_METRICS=false
LOG_LEVEL=INFO
```

### Port Configuration
- **Backend**: 8000 (configurable via `--port` flag)
- **Frontend**: 3000 (configurable via `pnpm dev --port 3001`)

---

## 🚨 Troubleshooting

### Common Issues

#### Poetry Not Found
```bash
# Add Poetry to PATH (Windows)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:APPDATA\Python\Scripts", "User")
```

#### Port Already in Use
```bash
# Change backend port
poetry run uvicorn app.main:app --reload --port 8001

# Change frontend port
pnpm dev --port 3001
```

#### Dependencies Installation Issues
```bash
# Clear Poetry cache
poetry cache clear . --all

# Reinstall dependencies
poetry install --no-cache
```

#### Docker Issues
```bash
# Rebuild without cache
docker-compose -f docker/compose.yaml build --no-cache

# Check Docker logs
docker-compose -f docker/compose.yaml logs
```

### Getting Help
- Check the logs in your terminal
- Verify all prerequisites are installed
- Ensure ports are not in use by other applications
- Check the `VALIDATION_SUMMARY.md` for detailed implementation status

---

## 📱 Usage Examples

### Web Interface
1. Open http://localhost:3000
2. Drag and drop a PDF file or paste a DOI/URL
3. Select theme (academic, minimal, corporate)
4. Click "Generate Presentation"
5. Download the PowerPoint file

### API Usage
```bash
# Upload PDF and generate presentation
curl -X POST "http://localhost:8000/v1/generate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@research_paper.pdf" \
  -F "theme=academic" \
  -F "max_bullets=6"
```

### CLI Usage
```bash
# Generate from PDF
poetry run python -m paperslide.cli generate --pdf paper.pdf --theme academic --out slides.pptx

# Generate with custom settings
poetry run python -m paperslide.cli generate --pdf paper.pdf --theme minimal --max-bullets 4 --out presentation.pptx
```

---

## ✅ Success Indicators

When running successfully, you should see:

### Backend
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Frontend
```
✓ Ready in 2.3s
- Local:        http://localhost:3000
- Network:      http://192.168.1.100:3000
```

### Docker
```
[+] Running 2/2
 ✔ Container slideforge-backend-1  Started
 ✔ Container slideforge-frontend-1 Started
```

---

**🎉 You're ready to convert research papers into PowerPoint presentations!**
