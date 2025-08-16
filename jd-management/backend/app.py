#!/usr/bin/env python3
"""
Flask Backend for Job Description Management System
Provides RESTful API endpoints for CRUD operations on job descriptions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import os


# Environment variables - update password below

app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Sarthak@9148',  # CHANGE THIS TO YOUR ACTUAL MYSQL PASSWORD
    'database': 'rectool_db',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def calculate_jd_aging(created_date):
    """Calculate the age of a job description in days"""
    try:
        if isinstance(created_date, str):
            created_date = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()
        age = (current_date - created_date).days
        return max(0, age)  # Return 0 if negative
    except:
        return 0

def create_tables():
    """Create the job_descriptions table if it doesn't exist"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create customer table first
        create_customer_table = """
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            customer_email VARCHAR(255),
            customer_phone VARCHAR(50),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create skillset_category table
        create_skillset_category_table = """
        CREATE TABLE IF NOT EXISTS skillset_category (
            category_id INT AUTO_INCREMENT PRIMARY KEY,
            category_name VARCHAR(255) NOT NULL UNIQUE,
            description TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create job_mode table
        create_job_mode_table = """
        CREATE TABLE IF NOT EXISTS job_mode (
            mode_id INT AUTO_INCREMENT PRIMARY KEY,
            mode_name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create job_status table
        create_job_status_table = """
        CREATE TABLE IF NOT EXISTS job_status (
            status_id INT AUTO_INCREMENT PRIMARY KEY,
            status_name VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create users table
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            role VARCHAR(100),
            is_active BOOLEAN DEFAULT TRUE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        # Create job_description table with foreign keys
        create_table_query = """
        CREATE TABLE IF NOT EXISTS job_description (
            jd_id INT AUTO_INCREMENT PRIMARY KEY,
            jd_title VARCHAR(255) NOT NULL,
            jd_customer_id INT NOT NULL,
            jd_consumer VARCHAR(255) NOT NULL,
            jd_original TEXT NOT NULL,
            jd_skillset_cat INT,
            jd_skillset JSON NOT NULL,
            jd_mode INT NOT NULL,
            jd_tenure INT NOT NULL,
            jd_op_exp_min DECIMAL(5,2) NOT NULL,
            jd_op_exp_max DECIMAL(5,2) NOT NULL,
            jd_op_budget_min DECIMAL(10,2) NOT NULL,
            jd_op_budget_max DECIMAL(10,2) NOT NULL,
            jd_open_position INT,
            jd_available_pos VARCHAR(100),
            jd_revenue_potential VARCHAR(255),
            jd_keywords JSON,
            jd_aging INT,
            jd_active BOOLEAN DEFAULT TRUE,
            jd_status INT DEFAULT 1,
            jd_created_by INT NOT NULL,
            jd_created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            jd_updated_by INT,
            jd_updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            jd_source TEXT,
            jd_special_instruction TEXT,
            
            -- Foreign Key Constraints
            CONSTRAINT fk_customer FOREIGN KEY (jd_customer_id) REFERENCES customer(customer_id),
            CONSTRAINT fk_skillset_category FOREIGN KEY (jd_skillset_cat) REFERENCES skillset_category(category_id),
            CONSTRAINT fk_job_mode FOREIGN KEY (jd_mode) REFERENCES job_mode(mode_id),
            CONSTRAINT fk_job_status FOREIGN KEY (jd_status) REFERENCES job_status(status_id),
            CONSTRAINT fk_created_by FOREIGN KEY (jd_created_by) REFERENCES users(user_id),
            CONSTRAINT fk_updated_by FOREIGN KEY (jd_updated_by) REFERENCES users(user_id)
        )
        """
        
        # Create all reference tables first
        cursor.execute(create_customer_table)
        cursor.execute(create_skillset_category_table)
        cursor.execute(create_job_mode_table)
        cursor.execute(create_job_status_table)
        cursor.execute(create_users_table)
        
        # Create job_description table last (due to foreign key dependencies)
        cursor.execute(create_table_query)
        
        connection.commit()
        print("✅ Database tables created successfully!")
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/jd', methods=['GET'])
def get_all_jobs():
    """GET /api/jd - Returns all Job Descriptions in JSON format"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                jd.*, 
                c.customer_name,
                sc.category_name as skillset_category_name,
                jm.mode_name as job_mode_name,
                js.status_name as job_status_name,
                u_created.full_name as created_by_name,
                u_updated.full_name as updated_by_name
            FROM job_description jd 
            JOIN customer c ON jd.jd_customer_id = c.customer_id 
            LEFT JOIN skillset_category sc ON jd.jd_skillset_cat = sc.category_id
            JOIN job_mode jm ON jd.jd_mode = jm.mode_id
            JOIN job_status js ON jd.jd_status = js.status_id
            JOIN users u_created ON jd.jd_created_by = u_created.user_id
            LEFT JOIN users u_updated ON jd.jd_updated_by = u_updated.user_id
            WHERE jd.jd_active = TRUE 
            ORDER BY jd.jd_created_date DESC
        """)
        jobs = cursor.fetchall()
        
        # Calculate aging for each job
        for job in jobs:
            if job['jd_created_date']:
                job['jd_aging'] = calculate_jd_aging(job['jd_created_date'])
        
        return jsonify({
            'success': True,
            'data': jobs,
            'count': len(jobs)
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/jd/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    """GET /api/jd/<id> - Returns a single Job Description by ID"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                jd.*, 
                c.customer_name,
                sc.category_name as skillset_category_name,
                jm.mode_name as job_mode_name,
                js.status_name as job_status_name,
                u_created.full_name as created_by_name,
                u_updated.full_name as updated_by_name
            FROM job_description jd 
            JOIN customer c ON jd.jd_customer_id = c.customer_id 
            LEFT JOIN skillset_category sc ON jd.jd_skillset_cat = sc.category_id
            JOIN job_mode jm ON jd.jd_mode = jm.mode_id
            JOIN job_status js ON jd.jd_status = js.status_id
            JOIN users u_created ON jd.jd_created_by = u_created.user_id
            LEFT JOIN users u_updated ON jd.jd_updated_by = u_updated.user_id
            WHERE jd.jd_id = %s AND jd.jd_active = TRUE
        """, (job_id,))
        job = cursor.fetchone()
        
        if not job:
            return jsonify({'error': 'Job description not found'}), 404
        
        # Calculate aging for the job
        if job['jd_created_date']:
            job['jd_aging'] = calculate_jd_aging(job['jd_created_date'])
        
        return jsonify({
            'success': True,
            'data': job
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/jd', methods=['POST'])
def create_job():
    """POST /api/jd - Creates a new Job Description"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['jd_title', 'jd_customer_id', 'jd_consumer', 'jd_original', 'jd_skillset', 'jd_mode', 'jd_tenure', 'jd_op_exp_min', 'jd_op_exp_max', 'jd_op_budget_min', 'jd_op_budget_max', 'jd_created_by']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Insert new job description
        insert_query = """
        INSERT INTO job_description (
            jd_title, jd_customer_id, jd_consumer, jd_original, jd_skillset_cat, 
            jd_skillset, jd_mode, jd_tenure, jd_op_exp_min, jd_op_exp_max, 
            jd_op_budget_min, jd_op_budget_max, jd_open_position, jd_available_pos,
            jd_revenue_potential, jd_keywords, jd_created_by, jd_source, jd_special_instruction
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            data['jd_title'],
            data['jd_customer_id'],
            data['jd_consumer'],
            data['jd_original'],
            data.get('jd_skillset_cat'),
            json.dumps(data['jd_skillset']) if isinstance(data['jd_skillset'], list) else data['jd_skillset'],
            data['jd_mode'],
            data['jd_tenure'],
            data['jd_op_exp_min'],
            data['jd_op_exp_max'],
            data['jd_op_budget_min'],
            data['jd_op_budget_max'],
            data.get('jd_open_position'),
            data.get('jd_available_pos'),
            data.get('jd_revenue_potential'),
            json.dumps(data.get('jd_keywords', [])) if isinstance(data.get('jd_keywords'), list) else data.get('jd_keywords'),
            data['jd_created_by'],
            data.get('jd_source'),
            data.get('jd_special_instruction')
        )
        
        cursor.execute(insert_query, values)
        connection.commit()
        
        new_job_id = cursor.lastrowid
        
        return jsonify({
            'success': True,
            'message': 'Job description created successfully',
            'data': {'jd_id': new_job_id}
        }), 201
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/jd/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """PUT /api/jd/<id> - Updates an existing Job Description"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Check if job exists
        cursor.execute("SELECT jd_id FROM job_description WHERE jd_id = %s AND jd_active = TRUE", (job_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Job description not found'}), 404
        
        # Build update query dynamically based on provided fields
        update_fields = []
        values = []
        
        # Map frontend field names to database field names
        field_mapping = {
            'jd_title': 'jd_title',
            'jd_customer_id': 'jd_customer_id',
            'jd_consumer': 'jd_consumer',
            'jd_original': 'jd_original',
            'jd_skillset_cat': 'jd_skillset_cat',
            'jd_skillset': 'jd_skillset',
            'jd_mode': 'jd_mode',
            'jd_tenure': 'jd_tenure',
            'jd_op_exp_min': 'jd_op_exp_min',
            'jd_op_exp_max': 'jd_op_exp_max',
            'jd_op_budget_min': 'jd_op_budget_min',
            'jd_op_budget_max': 'jd_op_budget_max',
            'jd_open_position': 'jd_open_position',
            'jd_available_pos': 'jd_available_pos',
            'jd_revenue_potential': 'jd_revenue_potential',
            'jd_keywords': 'jd_keywords',
            'jd_status': 'jd_status',
            'jd_source': 'jd_source',
            'jd_special_instruction': 'jd_special_instruction'
        }
        
        for frontend_field, db_field in field_mapping.items():
            if frontend_field in data:
                update_fields.append(f'{db_field} = %s')
                if frontend_field in ['jd_skillset', 'jd_keywords'] and isinstance(data[frontend_field], list):
                    values.append(json.dumps(data[frontend_field]))
                else:
                    values.append(data[frontend_field])
        
        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400
        
        # Add updated_by and job_id to values
        values.append(data.get('jd_updated_by', 'System'))
        values.append(job_id)
        
        update_query = f"UPDATE job_description SET {', '.join(update_fields)}, jd_updated_by = %s WHERE jd_id = %s"
        
        cursor.execute(update_query, values)
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Job description updated successfully'
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/jd/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """DELETE /api/jd/<id> - Deletes a Job Description"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Check if job exists
        cursor.execute("SELECT jd_id FROM job_description WHERE jd_id = %s AND jd_active = TRUE", (job_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Job description not found'}), 404
        
        # Soft delete - set active to false instead of hard delete
        cursor.execute("UPDATE job_description SET jd_active = FALSE, jd_status = 'Closed' WHERE jd_id = %s", (job_id,))
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': 'Job description deleted successfully'
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """GET /api/categories - Returns all skillset categories"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM skillset_category ORDER BY category_name")
        categories = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': categories,
            'count': len(categories)
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/modes', methods=['GET'])
def get_modes():
    """GET /api/modes - Returns all job modes"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM job_mode ORDER BY mode_name")
        modes = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': modes,
            'count': len(modes)
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    """GET /api/statuses - Returns all job statuses"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM job_status ORDER BY status_name")
        statuses = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': statuses,
            'count': len(statuses)
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    """GET /api/users - Returns all users"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE is_active = TRUE ORDER BY full_name")
        users = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': users,
            'count': len(users)
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/jd/update-aging', methods=['POST'])
def update_jd_aging():
    """POST /api/jd/update-aging - Updates aging for all job descriptions"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = connection.cursor()
        
        # Update aging for all active jobs
        update_query = """
        UPDATE job_description 
        SET jd_aging = DATEDIFF(CURDATE(), jd_created_date)
        WHERE jd_active = TRUE
        """
        
        cursor.execute(update_query)
        rows_affected = cursor.rowcount
        connection.commit()
        
        return jsonify({
            'success': True,
            'message': f'Updated aging for {rows_affected} job descriptions',
            'rows_affected': rows_affected
        }), 200
        
    except Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'job-description-api',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Job Description Management API',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/jd': 'Get all job descriptions',
            'GET /api/jd/<id>': 'Get job description by ID',
            'POST /api/jd': 'Create new job description',
            'PUT /api/jd/<id>': 'Update job description',
            'DELETE /api/jd/<id>': 'Delete job description',
            'POST /api/jd/update-aging': 'Update aging for all jobs',
            'GET /api/categories': 'Get all skillset categories',
            'GET /api/modes': 'Get all job modes',
            'GET /api/statuses': 'Get all job statuses',
            'GET /api/users': 'Get all users',
            'GET /health': 'Health check'
        }
    }), 200

if __name__ == '__main__':
    # Create database tables on startup
    if create_tables():
        print("🚀 Starting Flask Backend Server...")
        print("📱 API available at: http://localhost:5000")
        print("🔌 Health check: http://localhost:5000/health")
        print("📚 API docs: http://localhost:5000/")
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    else:
        print("❌ Failed to create database tables. Please check your MySQL connection.") 