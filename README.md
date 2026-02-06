# To-Do Project

A To-Do application with authentication and profile management features.

## Features

- **Add and remove tasks**
- **Mark tasks as completed**
- **Automatically saves tasks to the database**
- **Responsive design**
- **Built-in authentication system**
- **OAuth2 authentication**
- **Add or remove a profile picture**
- **Change a profile picture**

## Local installation

### Prerequisites

- Python 3.11+
- Git
- Docker (optional, recommended)

### Step 1: Clone the repository

```bash
git clone https://github.com/F3NCE-Dev/fastapi-to-do-app.git
cd fastapi-to-do-app
```

### Step 2: Install dependencies

Create a virtual environment

```bash
python -m venv venv

source venv/bin/activate # Linux/Mac
# or
venv/Scripts/activate # Windows
```

Install requirements

```bash
pip install -r requirements.txt
```

### Step 3: Create a file named *.env*

```bash
echo "" > .env
```

Fill it with the required environment variables

Example:

```bash
SECRET_KEY="Secret_Key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL="sqlite+aiosqlite:///backend/app.db"

DEFAULT_USER_PROFILE_PIC_DIR="backend/default_media"
DEFAULT_USER_PROFILE_PIC_IMAGE="default.png"
MEDIA_DIR="backend/media"
    
FRONTEND_ORIGINS=["http://localhost:5500", "http://127.0.0.1:5500"]
REDIRECT_URI="http://localhost:5500/frontend/index.html"
    
OAUTH_GOOGLE_CLIENT_ID="google_client_id"
OAUTH_GOOGLE_CLIENT_SECRET="google_client_secret"

OAUTH_GITHUB_CLIENT_ID="github_client_id"
OAUTH_GITHUB_CLIENT_SECRET="github_client_secret"

DEBUG_MODE=true
```

## Running the Application

### Option 1: Run with Docker (Recommended)

- **Make sure Docker is installed and running**

```bash
docker-compose up --build
```

- **Access the application**

Frontend:

```bash
http://localhost:5500
```

Backend API:

```bash
http://localhost:8000
```

### Option 2: Run locally (Development)

- **Run the backend**

```bash
cd backend
python run.py
cd ..
```

- **Run the frontend**

```bash
cd frontend
python -m http.server 5500
```

## Technologies used

### Backend

- **FastAPI**
- **SQLAlchemy**
- **aiosqlite**
- **Pydantic**
- **PyJWT**
- **passlib**
- **python-multipart**
- **httpx**
- **aiofiles**
- **Uvicorn**

### Frontend

- **HTML**
- **JavaScript**
- **Tailwind CSS**

### DevOps

- **Docker**
- **Docker Compose**
- **Nginx**
