# Complete Setup Instructions

## PostgreSQL Database Setup

### Option 1: Automated Setup (Recommended)

#### macOS/Linux:
```bash
chmod +x setup_database.sh
./setup_database.sh
```

#### Windows:
```powershell
.\setup_database.ps1
```

### Option 2: Manual Setup

#### 1. Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from: https://www.postgresql.org/download/windows/

#### 2. Create Database and User

Connect to PostgreSQL:
```bash
psql -U postgres
```

Run these SQL commands:
```sql
CREATE DATABASE nasdaq_sentiment_db;
CREATE USER admin WITH PASSWORD 'admin';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE nasdaq_sentiment_db TO admin;
\c nasdaq_sentiment_db
GRANT ALL ON SCHEMA public TO admin;
\q
```

## Backend Setup

### 1. Navigate to backend directory:
```bash
cd backend
```

### 2. Create virtual environment:
```bash
python -m venv venv
```

### 3. Activate virtual environment:

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies:
```bash
pip install -r requirements.txt
```

### 5. Verify database connection:
```bash
python manage.py check
```

### 6. Run migrations:
```bash
python manage.py migrate
```

This will create all necessary database tables including:
- User authentication tables
- Admin interface tables
- Session management
- Content types
- Your custom API models (when you add them)

### 7. Create superuser for admin access:
```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Username (e.g., `admin`)
- Email (optional)
- Password (enter twice)

### 8. Start the Django server:
```bash
python manage.py runserver
```

### 9. Access the Admin Interface:

Open your browser and go to:
```
http://localhost:8000/admin/
```

Login with the superuser credentials you just created.

## Frontend Setup

### 1. Navigate to frontend directory (new terminal):
```bash
cd frontend
```

### 2. Install dependencies:
```bash
npm install
```

### 3. Start the React development server:
```bash
npm start
```

The frontend will automatically open at `http://localhost:3000`

## Verify Everything Works

1. **Check Frontend**: Go to http://localhost:3000
   - You should see the React app with "Backend API Status"
   - Status should show "✓ Status: ok"

2. **Check Admin**: Go to http://localhost:8000/admin/
   - Login with your superuser credentials
   - You should see the Django admin dashboard with:
     - Authentication and Authorization section
     - Groups and Users management

3. **Check API**: Go to http://localhost:8000/api/health/
   - You should see JSON: `{"status":"ok","message":"API is running successfully"}`

## Database Connection String

The default connection is configured in `backend/.env`:
```
DATABASE_URL=postgresql://admin:admin@localhost:5432/nasdaq_sentiment_db
```

## Troubleshooting

### PostgreSQL connection refused:
- Make sure PostgreSQL is running: `pg_isready`
- macOS: `brew services start postgresql@15`
- Linux: `sudo systemctl start postgresql`
- Windows: Start from Services or pgAdmin

### "role 'admin' does not exist":
- Run the database creation SQL commands again
- Make sure you're connected to PostgreSQL as the postgres user

### Migration errors:
- Drop and recreate the database if needed:
  ```sql
  DROP DATABASE nasdaq_sentiment_db;
  CREATE DATABASE nasdaq_sentiment_db;
  GRANT ALL PRIVILEGES ON DATABASE nasdaq_sentiment_db TO admin;
  ```
- Then run migrations again

### Switch to SQLite for testing:
If you want to quickly test without PostgreSQL, edit `backend/.env`:
```
USE_SQLITE=True
```

Then run migrations again.

## Production Deployment

For production, you should:

1. **Change database password**: Update `DATABASE_URL` in environment variables
2. **Set secure SECRET_KEY**: Generate a new one for production
3. **Set DEBUG=False**: In production environment
4. **Configure ALLOWED_HOSTS**: Add your domain
5. **Use environment variables**: Never commit `.env` file
6. **Enable SSL**: For database connections
7. **Set up database backups**: Regular automated backups

## Admin Interface Features

The Django admin interface provides:

- **User Management**: Create, edit, and delete users
- **Group Management**: Organize users into permission groups
- **Permission System**: Fine-grained access control
- **Content Management**: Manage all your models (when you add them)
- **Activity Logs**: Track admin actions
- **Search and Filters**: Find records quickly
- **Bulk Actions**: Perform operations on multiple records

### Adding Models to Admin

When you create new models in `backend/api/models.py`, register them in `backend/api/admin.py`:

```python
from django.contrib import admin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ['field1', 'field2', 'created_at']
    search_fields = ['field1']
    list_filter = ['created_at']
```

## Next Steps

Now that everything is set up:

1. Start building your models in `backend/api/models.py`
2. Create API views in `backend/api/views.py`
3. Add React components in `frontend/src/components/`
4. Build your features!

Good luck! 🚀

