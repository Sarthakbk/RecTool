# JD Management System

A comprehensive job description management system built with Python Flask backend and React frontend.

## 🏗️ Project Structure

```
jd-management/
│
├── backend/                # Python Flask backend
│   ├── app.py               # Main Flask application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── config.py            # Database connection & environment config
│   ├── models/              # SQLAlchemy/MySQL models
│   │   └── job_description.py
│   ├── routes/              # API endpoints
│   │   └── jd_routes.py
│   ├── controllers/         # Business logic
│   │   └── jd_controller.py
│   ├── services/            # DB services & helpers
│   │   └── jd_service.py
│   └── utils/               # Utility functions
│       └── validators.py
│
├── frontend/                # ReactJS frontend
│   ├── public/              # Static assets
│   │   └── index.html
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── FormField.jsx
│   │   │   ├── SectionHeader.jsx
│   │   │   └── JDTable.jsx
│   │   ├── pages/           # Page-level components
│   │   │   ├── JDEntry.jsx  # JD Entry form (2-column layout)
│   │   │   └── JDReport.jsx # Report view/edit
│   │   ├── services/        # API calls
│   │   │   └── jdService.js
│   │   ├── styles/          # CSS/Tailwind files
│   │   │   └── index.css
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json         # Frontend dependencies
│   ├── tailwind.config.js   # TailwindCSS configuration
│   └── postcss.config.js    # PostCSS configuration
│
├── database/                # MySQL scripts
│   ├── schema.sql           # CREATE TABLE statements
│   └── seed.sql             # Sample data (optional)
│
├── README.md
└── .gitignore
```

## 🚀 Features

### Backend (Python Flask)
- **RESTful API** with comprehensive CRUD operations
- **SQLAlchemy ORM** with MySQL database
- **Data validation** with custom validators
- **Error handling** and logging
- **CORS support** for frontend integration
- **Blueprint architecture** for scalable routing

### Frontend (React)
- **Responsive design** with TailwindCSS
- **Two-column layout** for JD entry form
- **Real-time validation** and error handling
- **Search and filtering** capabilities
- **Pagination** for large datasets
- **Statistics dashboard** with visual indicators

### Database (MySQL)
- **Normalized schema** with proper relationships
- **Indexes** for optimal performance
- **Constraints** for data integrity
- **Full-text search** capabilities
- **Views and stored procedures** for complex queries

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask 2.3.3** - Web framework
- **SQLAlchemy** - ORM
- **PyMySQL** - MySQL connector
- **Marshmallow** - Serialization/validation
- **Flask-CORS** - Cross-origin support

### Frontend
- **React 18** - UI library
- **TailwindCSS** - Utility-first CSS
- **Axios** - HTTP client
- **React Router** - Navigation
- **React Hot Toast** - Notifications
- **Heroicons** - Icon library

### Database
- **MySQL 8.0+** - Relational database
- **UTF8MB4** character set support

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- MySQL 8.0 or higher
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd jd-management
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Database Setup
```bash
# Connect to MySQL and run schema
mysql -u your_username -p < ../database/schema.sql
```

### 4. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Set environment variables (optional)
cp .env.example .env
```

### 5. Environment Configuration
Create `.env` files in both backend and frontend directories:

**Backend (.env):**
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DEV_DATABASE_URL=mysql+pymysql://username:password@localhost/rectool_db
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:5000
```

## 🏃‍♂️ Running the Application

### Development Mode

#### Option 1: Run Separately
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm start
```

#### Option 2: Use Scripts (if available)
```bash
# Backend
cd backend
python app.py

# Frontend
cd frontend
npm start
```

### Production Mode
```bash
# Backend
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend
cd frontend
npm run build
# Serve the build folder with your web server
```

## 🌐 API Endpoints

### Job Descriptions
- `POST /api/jd/` - Create new JD
- `GET /api/jd/` - Get all JDs with pagination
- `GET /api/jd/<id>` - Get JD by ID
- `PUT /api/jd/<id>` - Update JD
- `DELETE /api/jd/<id>` - Delete JD
- `GET /api/jd/search` - Advanced search
- `GET /api/jd/statistics` - Get statistics

### Health Check
- `GET /health` - Backend health status
- `GET /api/jd/health` - API health status

## 📱 Frontend Routes

- `/` - Job Description Entry Form
- `/report` - Job Description Report & Management

## 🔧 Configuration

### Database Configuration
The system supports multiple database configurations:
- **Development**: Local MySQL instance
- **Production**: Production MySQL instance
- **Testing**: Test database for CI/CD

### CORS Configuration
CORS is enabled for development. Configure allowed origins for production.

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📊 Database Schema

The system includes:
- **job_descriptions** - Main JD table
- **users** - User management (optional)
- **job_status** - JD lifecycle tracking
- **Views** - Common query views
- **Stored Procedures** - Complex operations
- **Triggers** - Data integrity

## 🚀 Deployment

### Backend Deployment
1. Set production environment variables
2. Use Gunicorn or uWSGI
3. Configure reverse proxy (Nginx/Apache)
4. Set up SSL certificates

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve static files with web server
3. Configure API proxy

### Database Deployment
1. Set up MySQL server
2. Configure backups and replication
3. Set up monitoring and alerts

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
- Create an issue in the repository
- Check the documentation
- Review the API endpoints

## 🔄 Version History

- **v1.0.0** - Initial release with basic CRUD operations
- **v1.1.0** - Added search and filtering capabilities
- **v1.2.0** - Enhanced validation and error handling 