#!/usr/bin/env python3
"""
MySQL Configuration for RecTool JD Management System
Modify these settings to match your MySQL Workbench configuration
"""

# MySQL Database Configuration
MYSQL_CONFIG = {
    'host': 'localhost',        # Your MySQL host (usually localhost)
    'port': 3306,              # MySQL port (default is 3306)
    'user': 'root',            # Your MySQL username
    'password': 'password',    # Your MySQL password - CHANGE THIS!
    'database': 'rectool_db',  # Database name
    'charset': 'utf8mb4'
}

# Flask Configuration
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# Database URL (automatically generated from config above)
def get_database_url():
    """Generate database URL from configuration"""
    config = MYSQL_CONFIG
    return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

# Instructions for setup
SETUP_INSTRUCTIONS = """
🔧 MySQL Setup Instructions:

1. Open MySQL Workbench
2. Connect to your MySQL server
3. Run the SQL script: setup_mysql_database.sql
4. Update the password in mysql_config.py
5. Start the server: python mysql_server.py

📋 Database Details:
- Database Name: rectool_db
- Table Name: job_descriptions
- Connection: localhost:3306

🌐 Access Points:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/health
"""
