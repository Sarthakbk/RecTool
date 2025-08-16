# 🚀 Flask Backend for Job Description Management

A complete Flask backend API that provides RESTful endpoints for managing job descriptions with MySQL database integration.

## ✨ Features

- **RESTful API** with full CRUD operations
- **MySQL Database** integration with automatic table creation
- **CORS Support** for React frontend integration
- **Input Validation** and error handling
- **Proper HTTP Status Codes** for all responses
- **Array Handling** for secondary_skills (stored as comma-separated string in DB)

## 🏗️ API Endpoints

### 1. **GET /api/jd**
Returns all job descriptions in JSON format.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Senior React Developer",
      "primary_skill": "ReactJS",
      "secondary_skills": ["JavaScript", "TypeScript", "Node.js"],
      "experience_required": 5,
      "job_summary": "We are looking for a Senior React Developer...",
      "date_created": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### 2. **GET /api/jd/<id>**
Returns a single job description by ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Senior React Developer",
    "primary_skill": "ReactJS",
    "secondary_skills": ["JavaScript", "TypeScript", "Node.js"],
    "experience_required": 5,
    "job_summary": "We are looking for a Senior React Developer...",
    "date_created": "2024-01-15T10:30:00"
  }
}
```

### 3. **POST /api/jd**
Creates a new job description.

**Request Body:**
```json
{
  "title": "Python Developer",
  "primary_skill": "Python",
  "secondary_skills": ["Flask", "Django", "MySQL"],
  "experience_required": 3,
  "job_summary": "Join our Python development team..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Job description created successfully",
  "data": {
    "id": 2
  }
}
```

### 4. **PUT /api/jd/<id>**
Updates an existing job description.

**Request Body:**
```json
{
  "title": "Senior Python Developer",
  "experience_required": 5
}
```

**Response:**
```json
{
  "success": true,
  "message": "Job description updated successfully"
}
```

### 5. **DELETE /api/jd/<id>**
Deletes a job description.

**Response:**
```json
{
  "success": true,
  "message": "Job description deleted successfully"
}
```

### 6. **GET /health**
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "job-description-api",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 7. **GET /**
API information and documentation.

## 🗄️ Database Schema

The `job_descriptions` table has the following structure:

```sql
CREATE TABLE job_descriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    primary_skill VARCHAR(255) NOT NULL,
    secondary_skills TEXT,
    experience_required INT,
    job_summary TEXT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features:**
- `secondary_skills` is stored as a comma-separated string in MySQL
- Automatically converted to/from arrays in API responses
- `date_created` automatically set to current timestamp
- Proper indexes for performance

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- MySQL Workbench (optional, for database management)

### Step 1: Database Setup
1. **Install MySQL** if you haven't already
2. **Run the SQL script:**
   ```bash
   mysql -u root -p < database/create_job_descriptions_table.sql
   ```
   Or copy and paste the SQL commands into MySQL Workbench

### Step 2: Backend Setup
1. **Navigate to backend directory:**
   ```bash
   cd jd-management/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=rectool_db
   ```

### Step 3: Run the Server
```bash
python app.py
```

**Or use the batch file (Windows):**
```bash
run_flask_backend.bat
```

## 🌐 Access Points

- **API Base URL**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Documentation**: http://localhost:5000/
- **Frontend**: http://localhost:3000 (React app)

## 🔧 Configuration

### Environment Variables
All database configuration can be set via environment variables:

- `DB_HOST`: MySQL host (default: localhost)
- `DB_PORT`: MySQL port (default: 3306)
- `DB_USER`: MySQL username (default: root)
- `DB_PASSWORD`: MySQL password (required)
- `DB_NAME`: Database name (default: rectool_db)

### Database Connection
The backend automatically:
- Connects to MySQL using the configured credentials
- Creates the database and tables if they don't exist
- Handles connection pooling and cleanup
- Provides detailed error messages for connection issues

## 🧪 Testing the API

### Using curl
```bash
# Health check
curl http://localhost:5000/health

# Get all jobs
curl http://localhost:5000/api/jd

# Create a job
curl -X POST http://localhost:5000/api/jd \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Job","primary_skill":"Python","secondary_skills":["Flask","MySQL"]}'

# Get job by ID
curl http://localhost:5000/api/jd/1

# Update job
curl -X PUT http://localhost:5000/api/jd/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Job Title"}'

# Delete job
curl -X DELETE http://localhost:5000/api/jd/1
```

### Using Postman
1. Import the endpoints into Postman
2. Set base URL to `http://localhost:5000`
3. Test each endpoint with appropriate request bodies

## 🚨 Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data or missing required fields
- **404 Not Found**: Job description not found
- **500 Internal Server Error**: Database connection issues or server errors

All errors return JSON responses with descriptive messages.

## 🔄 Frontend Integration

### Update Frontend Configuration
Update your React frontend to connect to the new backend:

```javascript
// In your frontend service files
const API_BASE_URL = 'http://localhost:5000';

// Update package.json proxy
{
  "proxy": "http://localhost:5000"
}
```

### CORS Configuration
CORS is already enabled for all origins (`*`) to allow frontend integration.

## 📊 Sample Data

The SQL script includes sample job descriptions:
- Senior React Developer
- Python Backend Developer  
- Full Stack Developer

## 🚀 Production Deployment

For production use:

1. **Set production environment variables**
2. **Use Gunicorn or uWSGI:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
3. **Configure reverse proxy (Nginx/Apache)**
4. **Set up SSL certificates**
5. **Configure MySQL for production**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at http://localhost:5000/
- Review the error messages in the console
- Check MySQL connection and database setup
- Verify environment variables are set correctly

---

**Happy coding! 🚀**
