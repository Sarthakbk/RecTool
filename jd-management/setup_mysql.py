#!/usr/bin/env python3
"""
MySQL Setup Script for JD Management System
This script helps you set up MySQL database and connection
"""

import os
import sys
import getpass
from pathlib import Path

def create_env_file():
    """Create .env file with MySQL configuration"""
    print("🔧 Setting up MySQL configuration...")
    print("=" * 50)
    
    # Get MySQL connection details
    print("Enter MySQL connection details:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = input("Port (default: 3306): ").strip() or "3306"
    username = input("Username (default: root): ").strip() or "root"
    password = getpass.getpass("Password: ")
    database = input("Database name (default: rectool_db): ").strip() or "rectool_db"
    
    # Create .env file content
    env_content = f"""# MySQL Database Configuration
DEV_DATABASE_URL=mysql+pymysql://{username}:{password}@{host}:{port}/{database}

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
"""
    
    # Write .env file
    env_file = Path("backend/.env")
    env_file.parent.mkdir(exist_ok=True)
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Environment file created: {env_file}")
    return {
        'host': host,
        'port': port,
        'username': username,
        'password': password,
        'database': database
    }

def create_database_script(config):
    """Create SQL script to create database"""
    sql_content = f"""-- Create MySQL Database for RecTool
-- Run this script in MySQL to create the database

-- Create database
CREATE DATABASE IF NOT EXISTS {config['database']} 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE {config['database']};

-- Create job_descriptions table
CREATE TABLE IF NOT EXISTS job_descriptions (
    jd_id INT AUTO_INCREMENT PRIMARY KEY,
    jd_title VARCHAR(255) NOT NULL,
    primary_skill VARCHAR(100) NOT NULL,
    secondary_skills TEXT,
    mode ENUM('Onsite', 'Remote', 'Hybrid') NOT NULL,
    tenure_months INT NOT NULL,
    open_positions INT NOT NULL,
    available_positions INT NOT NULL DEFAULT 0,
    experience_min DECIMAL(4,1),
    experience_max DECIMAL(4,1),
    budget_min DECIMAL(10,2),
    budget_max DECIMAL(10,2),
    jd_keywords TEXT,
    original_jd LONGTEXT,
    special_instruction TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_jd_title (jd_title),
    INDEX idx_primary_skill (primary_skill),
    INDEX idx_mode (mode),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_search (jd_title, primary_skill, jd_keywords)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data
INSERT INTO job_descriptions (
    jd_title, primary_skill, secondary_skills, mode, tenure_months, 
    open_positions, available_positions, experience_min, experience_max, 
    budget_min, budget_max, jd_keywords, original_jd, special_instruction
) VALUES (
    'Senior React Developer',
    'ReactJS',
    'NodeJS, MySQL, TypeScript',
    'Hybrid',
    12,
    5,
    3,
    3.0,
    5.0,
    60000.00,
    90000.00,
    'React, JavaScript, Frontend',
    'We are looking for a Senior React Developer to join our dynamic team.',
    'Candidate must join within 30 days.'
);

-- Show the created table
DESCRIBE job_descriptions;

-- Show sample data
SELECT * FROM job_descriptions;
"""
    
    sql_file = Path("database/setup_mysql.sql")
    sql_file.parent.mkdir(exist_ok=True)
    
    with open(sql_file, 'w') as f:
        f.write(sql_content)
    
    print(f"✅ SQL script created: {sql_file}")
    return sql_file

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    
    requirements_file = Path("backend/requirements.txt")
    if requirements_file.exists():
        try:
            os.system(f"pip install -r {requirements_file}")
            print("✅ Dependencies installed successfully!")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
    else:
        print("❌ Requirements file not found!")

def main():
    """Main setup function"""
    print("🚀 MySQL Setup for JD Management System")
    print("=" * 50)
    
    # Check if MySQL is available
    try:
        import pymysql
        print("✅ PyMySQL is available")
    except ImportError:
        print("❌ PyMySQL not found. Installing...")
        os.system("pip install PyMySQL")
    
    # Create environment configuration
    config = create_env_file()
    
    # Create database script
    sql_file = create_database_script(config)
    
    # Install dependencies
    install_dependencies()
    
    print("\n" + "=" * 50)
    print("🎉 MySQL Setup Complete!")
    print("=" * 50)
    print("\n📋 Next Steps:")
    print("1. Start MySQL server")
    print("2. Run the SQL script to create database:")
    print(f"   mysql -u {config['username']} -p < {sql_file}")
    print("3. Start the MySQL server:")
    print("   python mysql_server.py")
    print("4. Start the frontend:")
    print("   cd frontend && npm start")
    print("\n🌐 Access your application:")
    print("   Frontend: http://localhost:3000")
    print("   Backend: http://localhost:5000")
    print("   Health: http://localhost:5000/health")

if __name__ == '__main__':
    main()
