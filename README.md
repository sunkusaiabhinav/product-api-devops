# Product Management API — Backend, Docker & CI/CD Pipeline

A production-minded, beginner-friendly REST API built with **Python 3.12**, **FastAPI**, **Pydantic**, **Pytest**, **Docker**, and **GitHub Actions**.

---

## 1. Project Overview

This repository demonstrates how to architect, develop, containerize, and test a modern Python backend service following industry best practices.

Key highlights:
- **RESTful Endpoints**: Full CRUD operations for managing a product catalog.
- **Strict Data Validation**: Pydantic models with custom validators preventing empty names and invalid pricing.
- **Automated Testing**: Comprehensive Pytest suite covering positive and negative edge cases with isolated test states.
- **Production Containerization**: Lightweight multi-stage Docker build utilizing official Python 3.12 slim images and non-root security.
- **Continuous Integration (CI)**: GitHub Actions workflow automating linting, testing, and Docker image validation on every push and pull request.

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3.12** | Core programming language |
| **FastAPI** | High-performance, asynchronous web framework |
| **Uvicorn** | Lightning-fast ASGI production web server |
| **Pydantic v2** | Data modeling, validation, and serialization |
| **Pytest** | Automated test suite framework |
| **HTTPX** | Fast ASGI test client for simulating HTTP calls |
| **Ruff** | Ultra-fast Python linter and code formatter |
| **Docker** | Application containerization and environment consistency |
| **GitHub Actions** | CI automation for linting, testing, and Docker builds |

---

## 3. Project Directory Structure

```text
product-api-devops/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow definition
├── app/
│   ├── __init__.py           # Package indicator
│   ├── main.py               # FastAPI application and route endpoints
│   ├── models.py             # Domain models and in-memory repository store
│   └── schemas.py            # Pydantic schemas for request validation & responses
├── tests/
│   ├── __init__.py           # Test package indicator
│   └── test_products.py      # Automated Pytest suite
├── .dockerignore              # Files excluded from Docker build context
├── .gitignore                # Files excluded from Git version control
├── Dockerfile                # Production Docker container blueprint
├── pyproject.toml            # Tool configuration for Ruff and Pytest
├── requirements.txt          # Pinned project dependencies
└── README.md                 # Complete project documentation
```

---

## 4. Prerequisites

Before running the project, ensure you have:
1. **Python 3.12+** installed (`python --version`)
2. **Git** installed (`git --version`)
3. **Docker Desktop** installed and running (`docker --version`, `docker ps`)

---

## 5. How to Create and Activate a Virtual Environment

Isolate your application dependencies within a dedicated virtual environment:

### Windows PowerShell:
```powershell
# Create virtual environment named .venv
python -m venv .venv

# Allow script execution if restricted (run once if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS / WSL:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

*(Your terminal prompt will now display `(.venv)`).*

---

## 6. How to Install Dependencies

Upgrade package manager and install pinned dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 7. How to Run the Backend Locally

Start the local Uvicorn development server with live reload enabled:

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Output:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

---

## 8. How to Access Swagger UI and Interactive Documentation

FastAPI automatically generates interactive OpenAPI documentation:

- **Swagger UI**: Open your browser at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - Allows executing live API requests directly from the browser.
- **ReDoc**: Open your browser at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Raw OpenAPI JSON**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 9. How to Run Automated Tests

Run the full automated test suite using Pytest:

```powershell
# Run all tests with verbose output
pytest

# Run tests showing extra details and print output
pytest -vv -s

# Run tests and stop on first failure
pytest -x
```

---

## 10. How to Run Ruff Checks

Validate code style, imports, and formatting:

```powershell
# Run Ruff lint checks
ruff check .

# Automatically fix fixable lint warnings
ruff check --fix .

# Verify code formatting
ruff format --check .

# Automatically reformat files to adhere to style guidelines
ruff format .
```

---

## 11. How to Build the Docker Image

Build the container image using the provided `Dockerfile`:

```powershell
docker build -t product-api:latest .
```

### Explanation of Docker Image vs Docker Container:
- **Docker Image**: A static, immutable, read-only package containing your application code, runtime (Python 3.12), libraries, environment configurations, and startup commands. Think of it as a blueprint, recipe, or virtual machine template.
- **Docker Container**: A live, running, isolated instance created from an image. You can instantiate multiple independent containers from a single Docker image. Think of it as a house built from the blueprint.

---

## 12. How to Run the Docker Container

Run the built image as an isolated container:

```powershell
docker run -d --name product-api-container -p 8000:8000 product-api:latest
```

Command breakdown:
- `-d`: Run in detached mode (background).
- `--name product-api-container`: Friendly name for identifying the container.
- `-p 8000:8000`: Maps port `8000` on your host machine to port `8000` inside the container.
- `product-api:latest`: The image tag to run.

---

## 13. How to Stop and Remove the Container

```powershell
# Stop the running container
docker stop product-api-container

# Remove the container
docker rm product-api-container

# (Or stop and remove in one step)
docker rm -f product-api-container
```

---

## 14. How to Test the Running Container

Once the container is running on port 8000, test the endpoints using PowerShell or `curl`:

### Health Check:
```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

# curl
curl -i http://localhost:8000/health
```

### Create a Product:
```powershell
# PowerShell
$body = @{
    name = "Ergonomic Chair"
    description = "High back mesh desk chair"
    price = 199.99
    in_stock = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/products" -Method Post -Body $body -ContentType "application/json"
```

### List All Products:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/products" -Method Get
```

### Get Single Product:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/products/1" -Method Get
```

### Update Product:
```powershell
$updateBody = @{
    price = 179.99
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/products/1" -Method Put -Body $updateBody -ContentType "application/json"
```

### Delete Product:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/products/1" -Method Delete
```

---

## 15. How the GitHub Actions CI Pipeline Works

The workflow defined in `.github/workflows/ci.yml` triggers automatically on:
1. Every `push` to the `main` branch.
2. Every `pull_request` targeting `main`.

### Pipeline Stages:

```text
[ Git Push / Pull Request ]
             │
             ▼
 ┌──────────────────────────────────────────┐
 │ Stage 1: Code Quality & Automated Tests │
 │  1. Checkout repository                  │
 │  2. Set up Python 3.12 (with pip cache)  │
 │  3. Install dependencies                 │
 │  4. Run Ruff lint and format check       │
 │  5. Run Pytest suite                     │
 └──────────────────────────────────────────┘
             │ (Passes)
             ▼
 ┌──────────────────────────────────────────┐
 │ Stage 2: Docker Image Build Validation   │
 │  1. Checkout repository                  │
 │  2. Set up Docker Buildx                 │
 │  3. Build Docker image (push: false)     │
 │  4. Smoke test container execution       │
 │     - Run container                      │
 │     - Query /health endpoint             │
 │     - Stop & clean up container          │
 └──────────────────────────────────────────┘
             │ (Passes)
             ▼
       [ CI SUCCESS ]
```

---

## 16. What Happens When a Test Fails

1. **Local Environment**:
   Pytest prints a descriptive failure report highlighting the failing assertion, line number, and expected vs actual values. The command exits with a non-zero exit code (`1`).
2. **GitHub Actions CI**:
   - The `Run Pytest test suite` step fails immediately.
   - The job `test-and-lint` halts.
   - Subsequent steps and dependent jobs (`build-docker`) are skipped.
   - The pull request or commit is marked with a red cross (❌).
   - Pull request merging can be blocked by branch protection rules.

---

## 17. What Happens When a Docker Build Fails

1. **Local Environment**:
   Docker terminates the build and outputs the specific line in the `Dockerfile` that caused the error (e.g. invalid syntax, missing dependency, failing healthcheck).
2. **GitHub Actions CI**:
   - The `build-docker` job fails.
   - The pipeline exits with failure status.
   - The bad Docker image is never generated, protecting downstream environments.

---

## 18. Limitations of In-Memory Storage

This initial version uses an in-memory dictionary (`ProductStore`) to manage products without requiring external database installation.

### Key Differences from Persistent Storage:
| Feature | In-Memory Storage (`dict` in RAM) | Persistent Database (PostgreSQL / SQLite) |
|---|---|---|
| **Data Durability** | **Volatile**: All data is lost immediately on container or server restart. | **Durable**: Data is written to disk / WAL and survives restarts, crashes, and redeployments. |
| **Scalability** | Cannot run multiple replicas (containers cannot share memory). | Multi-container replicas connect to the same shared database. |
| **Concurrency & ACID** | Basic in-process memory locks; risk of race conditions under heavy load. | Full ACID transactions, isolation levels, and row-level locks. |
| **Search & Indexing** | Linear in-memory scanning (`O(N)`). | B-Tree indexing, full-text search, and relational joins. |
| **Ideal For** | Unit tests, proof of concept, demos, rapid prototyping. | Production environments, audit logs, persistent customer data. |
