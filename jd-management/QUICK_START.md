# 🚀 Quick Start Guide - JD Management System

## 📋 Prerequisites

### Required Software:
1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download here](https://nodejs.org/)

### Installation Tips:
- ✅ Check "Add Python to PATH" during Python installation
- ✅ Restart your terminal after installing Python/Node.js

## 🏃‍♂️ Quick Start (3 Steps)

### Step 1: Install Python
```bash
# Download and install Python from python.org
# Make sure to check "Add Python to PATH"
```

### Step 2: Start the Backend Server
```bash
# Option A: Double-click the batch file
run_server.bat

# Option B: Command line
python simple_server.py
```

### Step 3: Start the Frontend
```bash
# Option A: Double-click the batch file
run_frontend.bat

# Option B: Command line
cd frontend
npm start
```

## 🌐 Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

## 🎯 What You'll See

### Frontend (Port 3000):
- ✅ **JD Entry Form**: Two-column layout for creating job descriptions
- ✅ **JD Report Page**: View and manage existing job descriptions
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Modern UI**: Clean interface with TailwindCSS

### Backend (Port 8000):
- ✅ **RESTful API**: Full CRUD operations for job descriptions
- ✅ **SQLite Database**: In-memory database with sample data
- ✅ **CORS Enabled**: Frontend can communicate with backend
- ✅ **Health Endpoints**: Monitor server status

## 🔧 API Endpoints Available

```
GET    /api/jd/              # Get all job descriptions
POST   /api/jd/              # Create new job description
GET    /api/jd/{id}          # Get specific job description
GET    /api/jd/statistics    # Get system statistics
GET    /health               # Health check
```

## 📱 Sample Data

The server comes with sample data:
- **Senior React Developer** position
- **Hybrid** work mode
- **12 months** tenure
- **5 open positions**, **3 available**

## 🚨 Troubleshooting

### Python Not Found:
```bash
# Install Python from python.org
# Make sure to check "Add Python to PATH"
# Restart your terminal
```

### Node.js Not Found:
```bash
# Install Node.js from nodejs.org
# Restart your terminal
```

### Port Already in Use:
```bash
# Change ports in the respective files
# Backend: simple_server.py (line with run_server(8000))
# Frontend: package.json (proxy field)
```

### Frontend Can't Connect to Backend:
```bash
# Make sure both servers are running
# Check that backend is on port 8000
# Verify CORS is enabled
```

## 🔄 Development Workflow

1. **Start Backend**: `python simple_server.py`
2. **Start Frontend**: `npm start` (in frontend directory)
3. **Make Changes**: Edit files in your code editor
4. **See Updates**: Frontend auto-reloads, backend needs restart
5. **Test API**: Use browser or tools like Postman

## 📚 Next Steps

Once you're comfortable with the simple server:
1. **Install MySQL** for production database
2. **Use Flask Backend**: `cd backend && pip install -r requirements.txt`
3. **Customize Schema**: Modify database/schema.sql
4. **Add Authentication**: Implement user login system
5. **Deploy**: Move to production server

## 🎉 You're Ready!

Your JD Management System is now running with:
- ✅ **Working Frontend** with React and TailwindCSS
- ✅ **Working Backend** with Python HTTP server
- ✅ **Sample Data** to test with
- ✅ **Full CRUD Operations** for job descriptions

Happy coding! 🚀 