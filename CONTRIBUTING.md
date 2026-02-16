# 🤝 Contributing to Transaction Manager

Thank you for your interest in contributing to **Transaction Manager**! This document provides guidelines and instructions for setting up a development environment, understanding the architecture, and contributing code.

## 📚 Table of Contents

- [Technologies Used](#technologies-used)
- [Architecture Overview](#architecture-overview)
- [Backend Layer Details](#backend-layer-details)
- [Frontend Layer Details](#frontend-layer-details)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Variables](#environment-variables)
  - [Run with Docker (recommended)](#run-with-docker-recommended)
  - [Run without Docker (backend only)](#run-without-docker-backend-only)
  - [Run without Docker (frontend only)](#run-without-docker-frontend-only)
  - [Install Pre-commit Hooks](#install-pre-commit-hooks)
- [Running Tests](#running-tests)
  - [Backend Tests](#backend-tests)
  - [Frontend Tests](#frontend-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)

---

## 🧰 Technologies Used

### Backend
- **FastAPI** – web framework
- **SQLAlchemy** – ORM
- **Pydantic** – data validation & settings
- **PostgreSQL** – database
- **Ruff** – linter & formatter
- **Mypy** – static type checker
- **Pytest** – testing

### Frontend
- **Vue 3** – framework
- **TypeScript** – language
- **Vite** – build tool
- **Pinia** – state management
- **Vue Router** – routing
- **Vitest** – unit testing
- **ESLint** – linter
- **Prettier** – formatter

### DevOps
- **Docker** & **Docker Compose** – containerization
- **GitHub Actions** – CI/CD

---

## 🏗️ Architecture Overview

The project follows a **clean architecture** approach with clear separation of concerns. Below is a high‑level diagram of the backend and frontend layers.

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (Vue 3)                        │
├───────────────┬─────────────────┬───────────────────────────────┤
│   Components  │     Stores      │          Services             │
│  (UI logic)   │  (Pinia state)  │   (API calls, helpers)        │
├───────────────┴─────────────────┴───────────────────────────────┤
│                        TypeScript Types                          │
│               (matching backend schemas)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP (REST)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend (FastAPI)                        │
├─────────────────────────────────────────────────────────────────┤
│                           Routers                                │
│   (endpoint definitions, request parsing, response formatting)   │
├─────────────────────────────────────────────────────────────────┤
│                           Services                               │
│   (business logic, validation, orchestration)                    │
├─────────────────────────────────────────────────────────────────┤
│                         Repositories                             │
│   (database queries, CRUD operations, domain object conversion)  │
├─────────────────────────────────────────────────────────────────┤
│                       Domain Models & Value Objects              │
│            (plain Python dataclasses, business entities)         │
├─────────────────────────────────────────────────────────────────┤
│                         Pydantic Schemas                         │
│   (request/response validation, serialization)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │  PostgreSQL │
                       └─────────────┘
```

### 🔍 Layer Responsibilities

#### Backend

- **Routers** (`app/api/`) – define HTTP endpoints, handle authentication (`Depends(get_current_user)`), parse request bodies/params, and call service methods. They return Pydantic models.
- **Services** (`app/services/`) – contain business logic, enforce domain rules (e.g., one‑way cash flow). They use repositories to fetch data and return domain objects or dictionaries.
- **Repositories** (`app/repositories/`) – abstract database access. They accept a SQLAlchemy session, query the database, and convert ORM objects to domain models (or dictionaries).
- **Domain Models** (`app/domain/models.py`) – plain Python dataclasses representing core entities (User, Contractor, Transaction, etc.).
- **Value Objects** (`app/domain/value_objects.py`) – immutable dataclasses for composite values (StatusPresentation, TransactionTypePresentation).
- **Pydantic Schemas** (`app/schemas/`) – define the shape of API requests and responses. They are used in routers and may contain validation logic.

#### Frontend

- **Components** (`src/components/`) – Vue single‑file components (`.vue`). They handle UI rendering and user interactions, and dispatch actions to stores.
- **Stores** (`src/stores/`) – Pinia stores that manage application state, call service functions, and update reactive data.
- **Services** (`src/services/`) – encapsulate API calls using Axios. They return typed promises.
- **Types** (`src/types/`) – TypeScript interfaces that mirror the backend Pydantic schemas, ensuring type safety across the frontend.

---

## 🛠️ Development Setup

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/) (for containerized development)
- [Node.js](https://nodejs.org/) 24+ and npm (if running frontend natively)
- [Python](https://www.python.org/) 3.14+ and `pip` (if running backend natively)
- [Pre-commit](https://pre-commit.com/) (will be installed later)

### Clone the Repository

```bash
git clone https://github.com/yourusername/TransactionManager.git
cd TransactionManager
```

### Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

The default values work for local Docker development. For native runs, adjust `DATABASE_URL` and `VITE_API_BASE_URL` as needed.

### Run with Docker (recommended)

This is the simplest way to get the full stack running.

```bash
docker-compose up -d
```

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Stop with `docker-compose down`.

### Run without Docker (backend only)

1. **Start PostgreSQL using Docker** (the only service needed):

   ```bash
   docker-compose up -d postgres
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or .\venv\Scripts\activate on Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -e .           # install the package in editable mode
   pip install types-passlib   # for mypy
   ```

4. **Start the server**:

   ```bash
   uvicorn app.main:app --reload
   ```

The backend will be available at `http://localhost:8000`.

### Run without Docker (frontend only)

1. **Install dependencies**:

   ```bash
   cd frontend
   npm install
   ```

2. **Create a `.env` file** (or copy from the root `.env`) with:

   ```
   VITE_API_BASE_URL=http://localhost:8000
   ```

3. **Start the dev server**:

   ```bash
   npm run dev
   ```

The frontend will be available at [http://localhost:5173](http://localhost:5173).

### Install Pre-commit Hooks

Pre-commit runs linters and type checkers automatically before each commit.

```bash
pip install pre-commit        # if not already installed
pre-commit install
```

Now every commit will trigger:

- Ruff (lint & format) on backend Python files
- Mypy on backend
- ESLint on frontend
- Prettier on frontend
- TypeScript check on frontend

You can also run all hooks manually:

```bash
pre-commit run --all-files
```

---

## 🧪 Running Tests

### Backend Tests

With Docker (database already running):

```bash
docker-compose exec backend pytest
```

Or natively (ensure `DATABASE_TEST_URL` is set and database is running):

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test:unit
```

For end‑to‑end tests (when implemented), you may need both backend and frontend running.

---

## 🔄 CI/CD Pipeline

We use GitHub Actions to automatically run checks on every push and pull request. The workflow (`.github/workflows/ci.yml`) consists of:

1. **Backend job**:
   - Sets up Python, installs dependencies.
   - Runs Ruff, Mypy, and Pytest against a fresh PostgreSQL service container.
   - Database init scripts are executed via `psql` before tests.

2. **Frontend job**:
   - Sets up Node, installs dependencies.
   - Runs ESLint, Prettier check, TypeScript check, and Vitest.

All checks must pass before merging.

---

## 📏 Coding Standards

- **Python**: Follow [PEP 8](https://peps.python.org/pep-0008/). Ruff and Mypy will enforce this.
- **TypeScript**: Use ESLint and Prettier configurations provided in the `frontend` directory.
- **Commit messages**: Write clear, concise messages. Use conventional commits if you like (e.g., `feat: add transaction search`).
- **Documentation**: Update this `CONTRIBUTING.md` or inline docstrings when adding new features.

---

## 🔀 Pull Request Process

1. **Fork** the repository and create a feature branch from `main`.
2. **Make your changes**, ensuring tests pass locally and pre-commit hooks succeed.
3. **Push** to your fork and open a pull request against the `main` branch.
4. In the PR description, explain what you changed and why.
5. **Ensure the CI pipeline passes** – if it fails, fix the issues.
6. A maintainer will review your PR. Address any feedback.

Thank you for contributing! 🎉
