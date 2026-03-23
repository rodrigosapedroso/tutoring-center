# Tutoring Center Platform

Built to solve a real-world problem: parents often lack visibility into their student's tutoring sessions unless they physically visit the center.

This platform centralizes attendance and student progress in a simple and accessible interface.

## MVP Goal

Enable parents to:
- Check if their child attended classes
- Track weekly performance and academic evolution

## User Profiles & Features

### Core Concept

The platform is centered around the **student**.

Each student can be associated with:
- One or more **teachers**
- One or more **parents** (or other responsible adults)

### Admin - Center Owner
- Create and manage students
- Create and assign teachers to students
- Create and assign parents to students
- Create and schedule classes (individual or group)
- View all classes, students, teachers and parents

### Teacher
- View assigned classes (calendar/agenda)
- Register class information (attendance, homework, etc.)
- Submit weekly evaluations

### Parent
- View all classes of their student(s) and access teacher records 
- View student performance by subject and week  
- Leave comments visible to the teacher and admin  

## Tech Stack
- **Frontend**: React 19 + TypeScript + Tailwind CSS
- **Backend**: Python 3.11+ + FastAPI + SQLAlchemy
- **Database**: PostgreSQL (default)

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+

### Database Setup (PostgreSQL)
1. Install and start PostgreSQL.
2. Create a database:
   ```bash
   createdb tutoring_center
   ```
   Or in psql: `CREATE DATABASE tutoring_center;`

3. Create a `backend/.env` file with your credentials based on the provided `.env.example` template:
   ```
   cp .env.example .env
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Seed the database (optional, for demo data):
   ```
   python seed.py
   ```
   - This will populate the database with sample teachers, students, and classes.

6. Start the server:
   ```
    cd backend
    python startup.py
    ```

    Alternatively, you can run the application directly with uvicorn:

    ```
    cd backend
    uvicorn app.main:app --reload
    ```
 
The API will be available at `http://127.0.0.1:8000`

API documentation: `http://127.0.0.1:8000/docs`

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
    npm run dev
    ```

   The application will be available at `http://localhost:5173`

## Project Structure
```
tutoring-center/
├── backend/
│   ├── app/
│   │   ├── __init__.py     # Turns app into a Python package
│   │   ├── main.py         # FastAPI application
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   └── routers.py      # API endpoints
│   ├── requirements.txt    # Python dependencies
│   ├── startup.py          # Starts the FastAPI server
│   ├── seed.py             # Database seeding script
│   ├── README.md
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main app component
│   │   ├── main.tsx        # Application entry point
│   │   ├── assets/         # Static assets: images, logos 
│   │   ├── components/     # Reusable React UI components
│   │   ├── hooks/          # Shared Logic and State Management
│   │   ├── pages/          # Page components
│   │   ├── services/       # API communication
│   │   └── types/          # Type definitions
│   ├── package.json        # Node dependencies
│   ├── README.md
│   └── .gitignore
├── README.md
└── .gitignore
```

## API Endpoints

