# ⚡ Quick Start Guide

Get your React + Django app running in 5 minutes!

## Prerequisites Check

```bash
# Check Python (need 3.8+)
python --version

# Check Node.js (need 16+)
node --version

# Check PostgreSQL
psql --version
```

If PostgreSQL is not installed:
- **macOS**: `brew install postgresql@15`
- **Ubuntu**: `sudo apt-get install postgresql postgresql-contrib`
- **Windows**: Download from https://www.postgresql.org/download/

---

## 🚀 Setup Commands (Copy & Paste)

### 1️⃣ Create Database

**macOS/Linux:**
```bash
chmod +x setup_database.sh
./setup_database.sh
```

**Windows (PowerShell):**
```powershell
.\setup_database.ps1
```

---

### 2️⃣ Start Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (choose your OS)
source venv/bin/activate          # macOS/Linux
# OR
venv\Scripts\activate             # Windows

# Install Python packages
pip install -r requirements.txt

# Create database tables
python manage.py migrate

# Create admin user (follow prompts)
python manage.py createsuperuser
# Suggested: username=admin, password=admin123 (for local dev)

# Start Django server
python manage.py runserver
```

Leave this terminal running! ✅

---

### 3️⃣ Start Frontend (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install Node packages
npm install

# Start React server
npm start
```

Browser will open automatically at http://localhost:3000 ✅

---

## 🎯 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **React App** | http://localhost:3000 | - |
| **Admin Panel** | http://localhost:8000/admin/ | Your superuser credentials |
| **API Health** | http://localhost:8000/api/health/ | - |
| **Django API** | http://localhost:8000/api/ | - |

---

## ✅ Verify Everything Works

1. **Frontend Test**: 
   - Go to http://localhost:3000
   - Should see "Backend API Status: ✓ ok"

2. **Admin Test**:
   - Go to http://localhost:8000/admin/
   - Login with your superuser credentials
   - Should see the Django admin dashboard

3. **API Test**:
   - Go to http://localhost:8000/api/health/
   - Should see: `{"status":"ok","message":"API is running successfully"}`

---

## 🛠️ Troubleshooting

### PostgreSQL won't connect?
```bash
# Check if PostgreSQL is running
pg_isready

# Start it if needed
brew services start postgresql@15  # macOS
sudo systemctl start postgresql    # Linux
```

### Database errors?
```bash
# Reset database (careful! deletes all data)
psql -U postgres -c "DROP DATABASE nasdaq_sentiment_db;"
psql -U postgres -c "CREATE DATABASE nasdaq_sentiment_db;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE nasdaq_sentiment_db TO admin;"

# Then re-run migrations
cd backend
python manage.py migrate
```

### Want to use SQLite instead?
Edit `backend/.env` and add:
```
USE_SQLITE=True
```
Then run migrations again.

### Port already in use?
```bash
# Backend (8000)
python manage.py runserver 8001

# Frontend (3000)
PORT=3001 npm start
```

---

## 🔄 Daily Development Workflow

After initial setup, you only need:

**Terminal 1:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python manage.py runserver
```

**Terminal 2:**
```bash
cd frontend
npm start
```

---

## 📚 Next Steps

Now that everything is running:

1. **Explore Admin**: Add users, groups, and permissions
2. **Create Models**: Add your data models in `backend/api/models.py`
3. **Build API**: Create views in `backend/api/views.py`
4. **Build Frontend**: Add React components in `frontend/src/`

See `README.md` for detailed documentation.

---

## 🆘 Need Help?

- **Full Instructions**: See `SETUP_INSTRUCTIONS.md`
- **Backend Help**: See `backend/README.md`
- **Frontend Help**: See `frontend/README.md`

**Database Info:**
- Name: `nasdaq_sentiment_db`
- User: `admin`
- Password: `admin`
- Host: `localhost:5432`

Happy coding! 🎉

