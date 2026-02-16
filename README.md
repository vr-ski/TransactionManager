# 💸 Transaction Manager

A modern, full‑stack application for managing financial transactions between contractors. Built with **Vue 3**, **TypeScript**, **FastAPI**, and **PostgreSQL**, containerized with **Docker**.

![Vue](https://img.shields.io/badge/Vue-3.x-4FC08D?logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-✓-2496ED?logo=docker)

## ✨ Features

- 🔐 **JWT authentication** – secure login and user sessions.
- 👥 **Contractor management** – create and view contractors.
- 💳 **Transaction management** – create, view, and update transaction statuses.
- 🔍 **Search & sort** – quickly find transactions by date, contractor, amount, or status.
- 📱 **Responsive UI** – clean, modern interface with a custom background.
- 🐳 **Dockerized** – run the entire stack with a single command.

## 🚀 Quick Start (Docker)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (with Compose)
- [Git](https://git-scm.com/)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/TransactionManager.git
cd TransactionManager
```

### 2. Set up environment variables

Copy the example environment file and adjust if needed (the defaults work for local development):

```bash
cp .env.example .env
```

### 3. Start the application

```bash
docker-compose up -d
```

This launches:

- **Frontend** at [http://localhost:3000](http://localhost:3000)
- **Backend API** at [http://localhost:8000](http://localhost:8000)
- **PostgreSQL** on port `5432`
- **Interactive API docs** at [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Access the app

Open your browser and go to [http://localhost:3000](http://localhost:3000).
Log in using the seeded test user:

- **Username:** `testuser`
- **Password:** `testpass123`

(You can find these credentials in the `db/init/02_mock_data.sql` file.)

## 🛠️ Useful Commands

- **Stop the application:**
  ```bash
  docker-compose down
  ```

- **View logs:**
  ```bash
  docker-compose logs -f
  ```

- **Rebuild after code changes:**
  ```bash
  docker-compose up -d --build
  ```

- **Run backend tests (inside container):**
  ```bash
  docker-compose exec backend pytest
  ```

- **Run frontend tests:**
  ```bash
  docker-compose exec frontend npm run test:unit
  ```

## 📁 Project Structure

```
.
├── backend/          # FastAPI application (Python)
├── frontend/         # Vue 3 + TypeScript application
├── db/               # PostgreSQL initialization scripts
├── docker-compose.yml
├── .env.example      # Environment variables template
└── README.md         # You are here!
```

## 🧪 Demo Credentials

| Username   | Password      | Role      |
|------------|---------------|-----------|
| `client` | `s3cre7P@ssW0rD!` | User 1    |
| `keyuser`     | `s3cre7P@ssW0rD!` | User 2    |

## 📚 API Documentation

Once the backend is running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on setting up a development environment, running tests, and coding standards.

## 📄 License

This project is licensed under the BSD 2-Clause – see the [LICENSE](LICENSE) file for details.

## ⭐️ Show your support

Give a ⭐️ if you like this project!
