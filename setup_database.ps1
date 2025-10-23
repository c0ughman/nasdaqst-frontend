# PowerShell script for Windows PostgreSQL setup
# Database setup script for Nasdaq Sentiment Tracker

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Database Setup (Windows)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Database credentials
$DB_NAME = "nasdaq_sentiment_db"
$DB_USER = "admin"
$DB_PASSWORD = "admin"

Write-Host "Creating PostgreSQL database and user..." -ForegroundColor Yellow
Write-Host ""

# Check if psql is available
try {
    $null = Get-Command psql -ErrorAction Stop
    Write-Host "PostgreSQL is installed!" -ForegroundColor Green
} catch {
    Write-Host "Error: PostgreSQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install PostgreSQL from: https://www.postgresql.org/download/windows/"
    exit 1
}

Write-Host ""
Write-Host "Creating database '$DB_NAME' and user '$DB_USER'..." -ForegroundColor Yellow
Write-Host ""

# Set password for psql command
$env:PGPASSWORD = "postgres"

# Create database and user (suppress errors if they already exist)
psql -U postgres -c "CREATE DATABASE $DB_NAME;" 2>$null
psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>$null
psql -U postgres -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';" 2>$null
psql -U postgres -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';" 2>$null
psql -U postgres -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';" 2>$null
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>$null
psql -U postgres -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $DB_USER;" 2>$null

Write-Host ""
Write-Host "✓ Database setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Database details:"
Write-Host "  Name: $DB_NAME"
Write-Host "  User: $DB_USER"
Write-Host "  Password: $DB_PASSWORD"
Write-Host "  Connection URL: postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5432/$DB_NAME"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Navigate to backend directory: cd backend"
Write-Host "  2. Create virtual environment: python -m venv venv"
Write-Host "  3. Activate virtual environment: venv\Scripts\activate"
Write-Host "  4. Install dependencies: pip install -r requirements.txt"
Write-Host "  5. Run migrations: python manage.py migrate"
Write-Host "  6. Create superuser: python manage.py createsuperuser"
Write-Host "  7. Start server: python manage.py runserver"
Write-Host ""
Write-Host "Admin interface will be available at: http://localhost:8000/admin/" -ForegroundColor Green
Write-Host ""

