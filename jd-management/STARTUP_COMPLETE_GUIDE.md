# 🚀 Complete Project Startup Guide - Frontend to Backend

## 📋 **Prerequisites Check**
Make sure you have these installed:
- ✅ **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- ✅ **Node.js 16+** - [Download here](https://nodejs.org/)
- ✅ **MySQL 8.0+** - [Download here](https://dev.mysql.com/downloads/mysql/)

## 🗄️ **Step 1: Database Setup**

### **Option A: Using MySQL Command Line**
```bash
# Connect to MySQL as root
mysql -u root -p

# Run the SQL script
source database/create_job_descriptions_table.sql

# Verify the table was created
USE rectool_db;
SHOW TABLES;
SELECT * FROM job_descriptions;
```

### **Option B: Using MySQL Workbench**
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Open the file: `database/create_job_descriptions_table.sql`
4. Execute the entire script
5. Verify the `rectool_db` database and `job_descriptions` table were created

## 🔧 **Step 2: Backend Setup & Start**

### **Option A: Use the Batch File (Easiest)**
```bash
# Double-click this file:
run_flask_backend.bat
```

### **Option B: Manual Setup**
```bash
# Navigate to backend directory
cd jd-management/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your MySQL password
echo DB_PASSWORD=your_mysql_password_here > .env

# Start the Flask server
python app.py
```

**Expected Output:**
```
✅ Database tables created successfully!
🚀 Starting Flask Backend Server...
📱 API available at: http://localhost:5000
🔌 Health check: http://localhost:5000/health
📚 API docs: http://localhost:5000/
```

## ⚛️ **Step 3: Frontend Setup & Start**

### **Option A: Use the Batch File**
```bash
# Double-click this file:
run_frontend.bat
```

### **Option B: Manual Setup**
```bash
# Navigate to frontend directory
cd jd-management/frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view jd-management-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

## 🌐 **Step 4: Access Your Application**

### **Backend API (Port 5000)**
- **Health Check**: http://localhost:5000/health
- **API Documentation**: http://localhost:5000/
- **All Jobs**: http://localhost:5000/api/jd
- **Single Job**: http://localhost:5000/api/jd/1

### **Frontend (Port 3000)**
- **Main Application**: http://localhost:3000
- **JD Entry Form**: http://localhost:3000/
- **JD Report Page**: http://localhost:3000/report

## 🧪 **Step 5: Test the Complete System**

### **Test Backend API**
```bash
# Health check
curl http://localhost:5000/health

# Get all jobs
curl http://localhost:5000/api/jd

# Create a new job
curl -X POST http://localhost:5000/api/jd \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Developer",
    "primary_skill": "JavaScript",
    "secondary_skills": ["React", "Node.js"],
    "experience_required": 2,
    "job_summary": "Test job description"
  }'
```

### **Test Frontend-Backend Connection**
1. Open http://localhost:3000 in your browser
2. Navigate to the JD Entry form
3. Fill out the form and submit
4. Check if the data appears in the Report page
5. Verify the data is stored in MySQL

## 🔄 **Complete Workflow**

### **Data Flow:**
```
Frontend (React) → Backend (Flask) → Database (MySQL)
     ↓                    ↓              ↓
  Port 3000         Port 5000      Port 3306
```

### **API Endpoints Working:**
- ✅ **GET /api/jd** - Frontend fetches all jobs
- ✅ **POST /api/jd** - Frontend creates new jobs
- ✅ **GET /api/jd/<id>** - Frontend fetches single job
- ✅ **PUT /api/jd/<id>** - Frontend updates jobs
- ✅ **DELETE /api/jd/<id>** - Frontend deletes jobs

## 🚨 **Troubleshooting**

### **Backend Issues:**
- **MySQL Connection Failed**: Check if MySQL is running and password is correct
- **Port 5000 in Use**: Change port in `app.py` or kill existing process
- **Dependencies Missing**: Run `pip install -r requirements.txt`

### **Frontend Issues:**
- **Port 3000 in Use**: Change port or kill existing React process
- **Can't Connect to Backend**: Verify backend is running on port 5000
- **CORS Errors**: Backend CORS is already configured

### **Database Issues:**
- **Table Not Found**: Run the SQL script again
- **Access Denied**: Check MySQL user permissions
- **Connection Refused**: Ensure MySQL service is running

## 📱 **What You Should See**

### **Backend Console:**
```
✅ Database tables created successfully!
🚀 Starting Flask Backend Server...
📱 API available at: http://localhost:5000
🔌 Health check: http://localhost:5000/health
📚 API docs: http://localhost:5000/
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### **Frontend Console:**
```
Compiled successfully!
Local: http://localhost:3000
```

### **Browser:**
- **Frontend**: Modern React app with TailwindCSS styling
- **Forms**: Working job description entry forms
- **Data**: Real-time data from MySQL database
- **API Calls**: Successful communication with Flask backend

## 🎯 **Quick Commands Summary**

```bash
# Terminal 1: Start Backend
cd jd-management
run_flask_backend.bat

# Terminal 2: Start Frontend  
cd jd-management
run_frontend.bat

# Or manually:
# Backend: cd backend && python app.py
# Frontend: cd frontend && npm start
```

## 🎉 **Success Indicators**

✅ **Backend**: Flask server running on port 5000  
✅ **Database**: MySQL connected with tables created  
✅ **Frontend**: React app running on port 3000  
✅ **API**: All endpoints responding correctly  
✅ **Integration**: Frontend successfully communicating with backend  
✅ **Data**: Job descriptions being created, read, updated, deleted  

---

**Your complete Job Description Management system is now running! 🚀**
