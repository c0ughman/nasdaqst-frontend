# React + Django Full Stack Application

A production-ready full-stack web application with React frontend and Django backend.

## Project Structure

```
.
├── backend/                 # Django backend
│   ├── config/             # Django project configuration
│   │   ├── settings.py     # Main settings file
│   │   ├── urls.py         # URL routing
│   │   ├── wsgi.py         # WSGI config for production
│   │   └── asgi.py         # ASGI config for async support
│   ├── api/                # Main API application
│   │   ├── views.py        # API views
│   │   ├── urls.py         # API URL routing
│   │   ├── models.py       # Database models
│   │   └── admin.py        # Admin interface configuration
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
│
└── frontend/               # React frontend
    ├── public/             # Static files
    ├── src/                # React source code
    │   ├── App.js          # Main application component
    │   ├── index.js        # Entry point
    │   └── services/       # API services
    │       └── api.js      # Axios configuration
    └── package.json        # Node dependencies
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Getting Started

### Step 1: PostgreSQL Database Setup

#### Automated Setup (Recommended)

**macOS/Linux:**
```bash
chmod +x setup_database.sh
./setup_database.sh
```

**Windows:**
```powershell
.\setup_database.ps1
```

This will create:
- Database: `nasdaq_sentiment_db`
- User: `admin`
- Password: `admin`

#### Manual Setup

See `SETUP_INSTRUCTIONS.md` for detailed manual setup steps.

### Step 2: Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
   Enter username: `admin`, email (optional), and password

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000`
**Admin interface:** `http://localhost:8000/admin/`

### Step 3: Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will be available at `http://localhost:3000`

### 🎉 Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/ (login with superuser credentials)
- **API Health**: http://localhost:8000/api/health/

## API Endpoints

### Health Check
- **GET** `/api/health/` - Check API status

### Admin Interface
- **URL**: `http://localhost:8000/admin/`
- Login with the superuser credentials you created
- Features:
  - User & Group Management
  - Permission System
  - Content Management (for all your models)
  - Activity Logs
  - Search & Filters

## Environment Variables

### Backend (.env)
The `.env` file is already created with default values:
```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://admin:admin@localhost:5432/nasdaq_sentiment_db
```

**For production**, change these values and never commit the `.env` file!

### Frontend (.env)
Copy `.env.example` to `.env` and update the values:
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Production Deployment

### Backend

1. Set environment variables:
   ```bash
   export DEBUG=False
   export DJANGO_SECRET_KEY=your-production-secret-key
   export ALLOWED_HOSTS=yourdomain.com
   ```

2. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

3. Use a production server like Gunicorn:
   ```bash
   gunicorn config.wsgi:application
   ```

### Frontend

1. Build the production bundle:
   ```bash
   npm run build
   ```

2. Serve the `build` directory using a web server (Nginx, Apache, etc.)

## Features

- ✅ Django REST Framework for API
- ✅ CORS configuration for cross-origin requests
- ✅ React with modern hooks
- ✅ Axios for API calls with interceptors
- ✅ Environment-based configuration
- ✅ Production-ready security settings
- ✅ Beautiful, responsive UI with gradient design
- ✅ Health check endpoint

## Tech Stack

### Backend
- Django 5.0.2
- Django REST Framework 3.14.0
- PostgreSQL (database)
- psycopg2-binary 2.9.9 (PostgreSQL adapter)
- django-cors-headers 4.3.1
- Gunicorn (production server)

### Frontend
- React 18.2.0
- Axios 1.6.7
- React Router DOM 6.22.0

## Development Tips

### Backend
- Run tests: `python manage.py test`
- Create migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Access Django shell: `python manage.py shell`

### Frontend
- Run tests: `npm test`
- Build for production: `npm run build`
- Eject configuration (not recommended): `npm run eject`

## Common Issues

### CORS Errors
Make sure the backend is running on `http://localhost:8000` and the frontend on `http://localhost:3000`. The CORS settings are configured for these ports.

### Module Not Found
- Backend: Make sure your virtual environment is activated
- Frontend: Run `npm install` to ensure all dependencies are installed

### Database Locked
If using SQLite, close any database browser tools that might have the database file open.

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Write tests for your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

