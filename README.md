# 🤖 Local AI Communicate(L.A.C)

A Flask REST API that lets authenticated users chat with a local LLM (via **Ollama** or **LM Studio**) and saves
conversation history in the database. Features JWT-based authentication, role-based permissions, and a PostgreSQL database.

---

## 📑 Table of Contents

- [🚀 Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📋 Prerequisites](#-prerequisites)
- [⚙️ Installation](#️-installation)
- [🔧 Configuration](#-configuration)
- [🏃 Running the App](#-running-the-app)
- [📡 API Endpoints](#-api-endpoints)
- [📬 Using Postman](#-using-postman)
- [🔐 User Permission Levels](#-user-permission-levels)
- [📂 Project Structure](#-project-structure)
- [🧰 Related Tools](#-related-tools)

---

## 🚀 Features

- ✅ User registration & login with hashed passwords
- 🔑 JWT Bearer token authentication
- 🛡️ Role-based access control (Basic → Admin)
- 💬 Chat with a local LLM (Ollama or LM Studio)
- 💾 Per-user chat history
- 🕵️ Admin endpoint to view all chat history

## 🛠️ Tech Stack

- **Python** / **Flask** / **Flask-RESTful**
- **SQLAlchemy** + **PostgreSQL**
- **Marshmallow** for request validation
- **PyJWT** for authentication
- **Ollama** or **LM Studio** as the local LLM backend

---

## 📋 Prerequisites

- **Python 3.10+**
- **PostgreSQL** running locally on port `5432`
- **Ollama** or **LM Studio** running locally
    - Ollama default: `http://localhost:11434`
    - LM Studio default: `http://localhost:1234`
- **Postman** (for testing the API)

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KaloyanVelev/Local_Ai_Communicate.git
   cd Local_Ai_Communicate
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *There may be libraries missing from the `requirements.txt` file. Make sure to install them manually if needed.*

## 🔧 Configuration

1. **Database Setup:**
   - Create a PostgreSQL database preferably named `Local_Ai_Communicate` on port `5432`.

2. **Environment Variables:**
   - In the`.env` file situated in the project root, add your database credentials and change the SECRET KEY:
     ```env
     DB_USER='your_postgres_user'
     DB_PASSWORD='your_postgres_password'
     SECRET_KEY='your_random_secret_key'
     ```
   - Note: By default, the app connects to the `postgres` database. You can change this in `main.py` if needed.
   

3. **LLM Service:**
   - Open `services/llm_service.py` and choose your preferred service at the most bottom of the code file:
     ```python
     llm_service = LMStudioService() # or OllamaService()
     #The default service selected is LMStudio if you are running ollama instead you should change it else the app wont work!!
     ```
## 🏃 Running the App

1. **Start the Flask server:**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:5000`.

## 📡 API Endpoints

| Method | Endpoint         | Description                   | Auth Required |
|:-------|:-----------------|:------------------------------|:--------------|
| `POST` | `/register`      | Register a new user           | ❌ No          |
| `POST` | `/login`         | Login and get JWT token       | ❌ No          |
| `GET`  | `/secret`        | Get current user info         | ✅ Yes         |
| `POST` | `/planUpgrade`   | Upgrade user plan             | ✅ Yes         |
| `GET`  | `/showUsers`     | List all users (Admin only)   | 👑 Yes (Admin) |
| `POST` | `/ai/chat`       | Chat with the LLM             | ✅ Yes         |
| `GET`  | `/ai/history/all`| View all chat history         | 👑 Yes (Admin) |
| `GET`  | `/`              | API Health Check/Test         | ❌ No          |

## 📬 Using Postman

To test the API using Postman, follow these steps:

1. **Set the Base URL:**
   - The API requests will be to `http://localhost:5000`.

2. **Authentication:**
   - In case a route requires authentication, go to the **Authorization** tab in Postman.
   - Select **Auth Type**: `Bearer Token`.
   - Paste the `token` received from the `/login` response.

### Request Templates

#### 1. Register a New User
- **Method:** `POST`
- **URL:** `http://localhost:5000/register`
- **Body:** `raw` (JSON)
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Password123"
}
```
*Note: Password must be at least 8 characters long and contain at least one uppercase letter.*

#### 2. Login
- **Method:** `POST`
- **URL:** `http://localhost:5000/login`
- **Body:** `raw` (JSON)
```json
{
    "username": "testuser",
    "password": "Password123"
}
```
*Copy the `token` from the response to use in latter requests.*

#### 3. Chat with AI
- **Method:** `POST`
- **URL:** `http://localhost:5000/ai/chat`
- **Auth:** `Bearer Token`
- **!!!Headers!!!:** `Content-Type: application/json`
- **Body:** `raw` (JSON)
```json
{
    "query": "Hello, how are you today?"
}
```
-**Note:** if you don't include the 'Content-Type' header, the request will most likely fail.

-**Note:** For now the app is fixated on a singular AI model named `qwen3.5:9b` so to test it you need to have this model installed locally. 
   - Or change it to whatever you want in `services/llm_service.py` in the class of the service you are using whether it be `LMStudioService` or `OllamaService`.

#### 4. Upgrade Plan
- **Method:** `POST`
- **URL:** `http://localhost:5000/planUpgrade`
- **Auth:** `Bearer Token`
- **Body:** `raw` (JSON)
```json
{
    "upgrade_to": "PLUS_USER"
}
```
*Available levels: `BASIC_USER`, `PLUS_USER`, `PRO_USER`, `ENTERPRISE_USER`, `ADMIN_USER`.*

#### 5. Get Private Info
- **Method:** `GET`
- **URL:** `http://localhost:5000/secret`
- **Auth:** `Bearer Token`

#### 6. List All Users (Admin Only)
- **Method:** `GET`
- **URL:** `http://localhost:5000/showUsers`
- **Auth:** `Bearer Token`

#### 7. View All Chat History (Admin Only)
- **Method:** `GET`
- **URL:** `http://localhost:5000/ai/history/all`
- **Auth:** `Bearer Token`

## 🔐 User Permission Levels

Users can have different levels which may be used to restrict or enable features:
- `BASIC_USER`
- `PLUS_USER`
- `PRO_USER`
- `ENTERPRISE_USER`
- `ADMIN_USER`

## 📂 Project Structure

```
Local_Ai_Communicate/
├── managers/            # Business logic layer
│   ├── auth.py          # JWT encoding/decoding, token verification
│   ├── chat_history.py  # AI chat history CRUD
│   └── user.py          # User registration, login, permissions
├── models/              # SQLAlchemy database models
│   ├── ai.py            # AIChatHistoryModel
│   ├── enums.py         # UserLevel enum
│   └── user.py          # UserModel
├── resources/           # Flask-RESTful resource endpoints
│   ├── ai.py            # AI chat & history resources
│   ├── routes.py        # Route registration
│   └── user.py          # User-related resources
├── schemas/             # Marshmallow validation schemas
│   ├── request/         # Request validation (ai, auth)
│   ├── response/        # Response serialization
│   └── bases.py         # Base schemas & password validation
├── services/
│   └── llm_service.py   # Ollama & LM Studio integrations
├── utils/
│   └── decorator.py     # Permission & schema validation decorators
├── .env                 # Environment variables (not committed)
├── database.py          # SQLAlchemy instance
├── main.py              # App factory & entry point
└── requirements.txt     # Python dependencies
```

## 🧰 Related Tools

- 🐘 [PostgreSQL](https://www.postgresql.org/) - Robust open-source relational database.
- 📬 [Postman](https://www.postman.com/) - Recommended for testing the API endpoints.
- 🦙 [Ollama](https://ollama.ai/) - Local LLM desktop app.
- 🖥️ [LM Studio](https://lmstudio.ai/) - Local LLM desktop app.


## The Project isn't fully complete!
### I am actively working on improving it and adding more features!
### In case you want to contact me, you can reach me at [kaloqnvelev1@gmail.com](mailto:kaloqnvelev1@gmail.com)