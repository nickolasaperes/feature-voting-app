# Feature Voting System - Backend

A Django-based REST API for a feature voting system where users can submit feature requests and vote on them. Built with Django, PostgreSQL, and Docker for easy deployment and development.

## 🚀 Features

- **Feature Management**: Create, read, update, and delete feature requests
- **Voting System**: Upvote and downvote features with real-time vote counting
- **Search Functionality**: Search features by title and description
- **Sorting & Filtering**: Features sorted by votes and creation date
- **RESTful API**: Clean, well-documented API endpoints
- **No Authentication**: Simple, open voting system
- **Docker Support**: Containerized for easy development and deployment
- **Comprehensive Tests**: Full test coverage for models, views, and API endpoints

## 🛠️ Tech Stack

- **Framework**: Django 5.2.4
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose
- **Testing**: Django Test Framework with Coverage
- **Code Quality**: Python best practices, type hints, and clean architecture

## 📋 Prerequisites

- Docker and Docker Compose installed
- Git for version control
- (Optional) Python 3.11+ for local development

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd feature-voting-backend
```

### 2. Environment Setup
Create a .env file in the project root:

```bash
# Database Configuration
DB_NAME=feature_voting
DB_USER=postgres
DB_PASSWORD=postgres123
DB_HOST=db
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. Build and Run with Docker 

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```


### 4. Run Database Migrations 

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 5. Access the API
The API will be available at: http://localhost:8000/api/
