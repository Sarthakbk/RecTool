# 🗄️ MySQL Workbench Setup Guide

## 📋 Step-by-Step Instructions

### Step 1: Open MySQL Workbench
1. Open MySQL Workbench on your computer
2. Connect to your MySQL server (usually localhost:3306)

### Step 2: Create Database and Table
1. In MySQL Workbench, open a new query tab
2. Copy and paste the contents of `setup_mysql_database.sql`
3. Click the lightning bolt icon to execute the script
4. You should see:
   - Database `rectool_db` created
   - Table `job_descriptions` created
   - Sample data inserted

### Step 3: Update Configuration
1. Open `mysql_config.py` in your code editor
2. Update the password line:
   ```python
   'password': 'YOUR_ACTUAL_MYSQL_PASSWORD',  # Change this!
   ```
3. Save the file

### Step 4: Start the Server
1. Open terminal in the `jd-management` directory
2. Run: `python mysql_server.py`
3. You should see: "✅ MySQL database tables created successfully!"

### Step 5: Start the Frontend
1. Open a new terminal
2. Navigate to: `cd frontend`
3. Run: `npm start`

## 🌐 Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 📊 Database Details

- **Database Name**: `rectool_db`
- **Table Name**: `job_descriptions`
- **Connection**: localhost:3306

## ✅ Test the Connection

1. Fill out a job description form in the frontend
2. Click "SAVE"
3. Check MySQL Workbench - you should see the new record in the `job_descriptions` table

## 🔧 Troubleshooting

### If you get connection errors:
1. Make sure MySQL is running
2. Check your password in `mysql_config.py`
3. Verify the database `rectool_db` exists
4. Check that the table `job_descriptions` was created

### If the server won't start:
1. Make sure all dependencies are installed: `pip install -r backend/requirements.txt`
2. Check that MySQL is running on port 3306
3. Verify your MySQL credentials

## 📝 Sample Data

The system will automatically create a sample job description:
- **Title**: Senior React Developer
- **Primary Skill**: ReactJS
- **Mode**: Hybrid
- **Tenure**: 12 months
- **Open Positions**: 5

## 🎯 What Happens When You Save

When you submit a job description from the frontend:
1. Data is sent to the Flask API (port 5000)
2. API validates the data
3. Data is saved to MySQL database (`rectool_db.job_descriptions`)
4. You'll see a success message
5. The data appears in MySQL Workbench immediately

## 🔍 View Data in MySQL Workbench

To see your saved data in MySQL Workbench:
```sql
USE rectool_db;
SELECT * FROM job_descriptions ORDER BY created_at DESC;
```

