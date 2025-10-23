#!/bin/bash

# Database setup script for Nasdaq Sentiment Tracker
# This script creates the PostgreSQL database and user

echo "========================================="
echo "PostgreSQL Database Setup"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Database credentials
DB_NAME="nasdaq_sentiment_db"
DB_USER="admin"
DB_PASSWORD="admin"

echo -e "${YELLOW}Creating PostgreSQL database and user...${NC}"
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}Error: PostgreSQL is not installed or not in PATH${NC}"
    echo "Please install PostgreSQL first:"
    echo "  - macOS: brew install postgresql@15"
    echo "  - Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    echo "  - Windows: Download from https://www.postgresql.org/download/windows/"
    exit 1
fi

# Check if PostgreSQL service is running
if ! pg_isready &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL service is not running. Attempting to start...${NC}"
    
    # Try to start PostgreSQL based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services start postgresql@15 || brew services start postgresql
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo systemctl start postgresql
    fi
    
    sleep 2
    
    if ! pg_isready &> /dev/null; then
        echo -e "${RED}Failed to start PostgreSQL. Please start it manually.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}PostgreSQL is running!${NC}"
echo ""

# Create database and user
echo "Creating database '$DB_NAME' and user '$DB_USER'..."
echo ""

# Try to create database and user (suppress errors if they already exist)
psql -U postgres -c "CREATE DATABASE $DB_NAME;" 2>/dev/null
psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null
psql -U postgres -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';" 2>/dev/null
psql -U postgres -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';" 2>/dev/null
psql -U postgres -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';" 2>/dev/null
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null

# Connect to the new database and grant schema permissions
psql -U postgres -d $DB_NAME -c "GRANT ALL ON SCHEMA public TO $DB_USER;" 2>/dev/null

echo ""
echo -e "${GREEN}✓ Database setup complete!${NC}"
echo ""
echo "Database details:"
echo "  Name: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo "  Connection URL: postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Navigate to backend directory: cd backend"
echo "  2. Activate virtual environment: source venv/bin/activate"
echo "  3. Install dependencies: pip install -r requirements.txt"
echo "  4. Run migrations: python manage.py migrate"
echo "  5. Create superuser: python manage.py createsuperuser"
echo "  6. Start server: python manage.py runserver"
echo ""
echo -e "${GREEN}Admin interface will be available at: http://localhost:8000/admin/${NC}"
echo ""

