#!/usr/bin/env python3
"""
Clean Flask Backend for Job Description Management System
Simple, working API endpoints with SQLite database storage
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)

# Enable CORS for React frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Database configuration
DATABASE = 'jd_database.db'

def init_database():
    """Initialize the SQLite database with proper table structure"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create job_descriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_descriptions (
            jd_id INTEGER PRIMARY KEY AUTOINCREMENT,
            jd_title TEXT NOT NULL,
            jd_customer_id TEXT,
            jd_consumer TEXT,
            jd_original TEXT NOT NULL,
            jd_skillset_cat INTEGER,
            jd_skillset TEXT,  -- JSON string
            jd_mode INTEGER,
            jd_tenure INTEGER,
            jd_op_exp_min REAL,
            jd_op_exp_max REAL,
            jd_op_budget_min REAL,
            jd_op_budget_max REAL,
            jd_open_position INTEGER,
            jd_available_pos TEXT,
            jd_revenue_potential TEXT,
            jd_currency TEXT DEFAULT 'USD',  -- Currency: USD or INR
            jd_keywords TEXT,  -- JSON string
            jd_source TEXT,
            jd_special_instruction TEXT,
            jd_created_by TEXT,
            jd_status INTEGER DEFAULT 1,
            jd_aging INTEGER DEFAULT 0,  -- Aging in days
            jd_created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            jd_updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT,
            customer_phone TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create skillset_categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skillset_categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL,
            description TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create engagement_modes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS engagement_modes (
            mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode_name TEXT NOT NULL,
            description TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data
    cursor.execute('''
        INSERT OR IGNORE INTO customers (customer_id, customer_name, customer_email) 
        VALUES (1, 'Sample Company', 'hr@samplecompany.com')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO skillset_categories (category_id, category_name, description) VALUES 
        (1, 'Frontend Development', 'Frontend technologies and frameworks'),
        (2, 'Backend Development', 'Backend technologies and frameworks'),
        (3, 'Full Stack Development', 'Both frontend and backend technologies'),
        (4, 'DevOps', 'DevOps and infrastructure technologies'),
        (5, 'Data Science', 'Data science and AI technologies'),
        (6, 'Mobile Development', 'Mobile app development technologies')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO engagement_modes (mode_id, mode_name, description) VALUES 
        (1, 'Remote', 'Work from anywhere'),
        (2, 'Onsite', 'Work at office location'),
        (3, 'Hybrid', 'Combination of remote and onsite work'),
        (4, 'Contract', 'Contract-based work arrangement'),
        (5, 'Part-time', 'Part-time work arrangement')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, full_name, email, role) VALUES 
        (1, 'nikitha', 'Nikitha', 'nikitha@company.com', 'HR'),
        (2, 'gauthami', 'Gauthami', 'gauthami@company.com', 'HR')
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized with tables and sample data")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/jd/scan', methods=['POST'])
def scan_job_description():
    """POST /api/jd/scan - Analyze JD text and extract relevant information"""
    try:
        data = request.get_json()
        if not data or 'jd_text' not in data:
            return jsonify({'error': 'JD text is required'}), 400
        
        jd_text = data['jd_text'].lower()
        
        # Initialize extracted data
        extracted_data = {}
        
        # Extract job title (look for common patterns)
        title_patterns = [
            r'(?:looking for|seeking|hiring|position|role|job|opportunity)[:\s]+([^.\n]+)',
            r'([a-z\s]+(?:developer|engineer|analyst|manager|specialist|consultant|architect|lead|senior|junior)[^.\n]*)',
            r'([a-z\s]+(?:developer|engineer|analyst|manager|specialist|consultant|architect|lead|senior|junior))'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, jd_text)
            if match:
                extracted_data['jd_title'] = match.group(1).strip().title()
                break
        
        # Enhanced skills extraction with better categorization
        skills = []
        
        # Programming Languages
        programming_languages = [
            'javascript', 'typescript', 'python', 'java', 'c#', 'c++', 'c', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'haskell', 'elixir', 'clojure', 'f#'
        ]
        
        # Frontend Technologies
        frontend_tech = [
            'react', 'angular', 'vue', 'svelte', 'ember', 'backbone', 'jquery', 'html', 'css', 'sass', 'less',
            'bootstrap', 'tailwind', 'material-ui', 'ant design', 'chakra ui', 'styled-components', 'emotion',
            'webpack', 'vite', 'parcel', 'babel', 'eslint', 'prettier', 'jest', 'cypress', 'playwright'
        ]
        
        # Backend Technologies
        backend_tech = [
            'node.js', 'express', 'koa', 'hapi', 'fastify', 'nest', 'django', 'flask', 'fastapi', 'tornado',
            'spring', 'hibernate', 'struts', 'play', 'quarkus', 'micronaut', 'laravel', 'symfony', 'codeigniter',
            'asp.net', '.net core', 'entity framework', 'dapper', 'xamarin', 'blazor'
        ]
        
        # Databases
        databases = [
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'sqlite',
            'oracle', 'sql server', 'mariadb', 'neo4j', 'influxdb', 'couchdb', 'firebase', 'supabase'
        ]
        
        # Cloud & DevOps
        cloud_devops = [
            'aws', 'azure', 'gcp', 'heroku', 'digitalocean', 'linode', 'vultr', 'docker', 'kubernetes',
            'terraform', 'ansible', 'chef', 'puppet', 'jenkins', 'gitlab', 'github', 'bitbucket', 'circleci',
            'travis', 'github actions', 'azure devops', 'jira', 'confluence', 'trello', 'asana', 'slack', 'teams'
        ]
        
        # Data Science & AI
        data_science = [
            'machine learning', 'ml', 'ai', 'artificial intelligence', 'deep learning', 'neural networks',
            'data science', 'big data', 'hadoop', 'spark', 'kafka', 'airflow', 'pandas', 'numpy', 'scikit-learn',
            'tensorflow', 'pytorch', 'keras', 'opencv', 'nltk', 'spacy', 'tableau', 'power bi', 'looker'
        ]
        
        # Mobile Development
        mobile_tech = [
            'react native', 'flutter', 'xamarin', 'ios', 'android', 'swift', 'kotlin', 'objective-c',
            'java android', 'cordova', 'phonegap', 'ionic', 'xcode', 'android studio'
        ]
        
        # All skills combined for searching
        all_skills = programming_languages + frontend_tech + backend_tech + databases + cloud_devops + data_science + mobile_tech
        
        # Extract skills from text
        for skill in all_skills:
            if skill in jd_text:
                skills.append(skill)
        
        # Also look for skills with common variations
        skill_variations = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'dotnet': '.net',
            'asp': 'asp.net',
            'ml': 'machine learning',
            'dl': 'deep learning',
            'ds': 'data science',
            'db': 'database',
            'sql': 'sql database',
            'nosql': 'nosql database'
        }
        
        for variation, full_name in skill_variations.items():
            if variation in jd_text and full_name not in skills:
                skills.append(full_name)
        
        extracted_data['jd_skillset'] = skills[:15]  # Limit to top 15 skills
        
        # Enhanced skillset category detection
        frontend_count = sum(1 for skill in skills if skill in frontend_tech)
        backend_count = sum(1 for skill in skills if skill in backend_tech)
        data_count = sum(1 for skill in skills if skill in data_science)
        devops_count = sum(1 for skill in skills if skill in cloud_devops)
        mobile_count = sum(1 for skill in skills if skill in mobile_tech)
        
        if frontend_count > 0 and backend_count > 0:
            extracted_data['jd_skillset_cat'] = 3  # Full Stack Development
        elif frontend_count > backend_count:
            extracted_data['jd_skillset_cat'] = 1  # Frontend Development
        elif backend_count > frontend_count:
            extracted_data['jd_skillset_cat'] = 2  # Backend Development
        elif data_count > 2:
            extracted_data['jd_skillset_cat'] = 5  # Data Science
        elif devops_count > 2:
            extracted_data['jd_skillset_cat'] = 4  # DevOps
        elif mobile_count > 1:
            extracted_data['jd_skillset_cat'] = 6  # Mobile Development
        else:
            extracted_data['jd_skillset_cat'] = 3  # Default to Full Stack
        
        # Extract work mode
        if any(word in jd_text for word in ['remote', 'work from home', 'wfh', 'telecommute']):
            extracted_data['jd_mode'] = 1  # Remote
        elif any(word in jd_text for word in ['onsite', 'office', 'location', 'on-site']):
            extracted_data['jd_mode'] = 2  # Onsite
        elif any(word in jd_text for word in ['hybrid', 'flexible', 'part remote']):
            extracted_data['jd_mode'] = 3  # Hybrid
        elif any(word in jd_text for word in ['contract', 'temporary', 'freelance', 'consulting']):
            extracted_data['jd_mode'] = 4  # Contract
        elif any(word in jd_text for word in ['part-time', 'part time', 'parttime']):
            extracted_data['jd_mode'] = 5  # Part-time
        
        # Extract tenure/duration
        tenure_patterns = [
            r'(\d+)\s*(?:month|months|mo)',
            r'(\d+)\s*(?:year|years|yr)',
            r'(\d+)\s*(?:week|weeks|wk)',
            r'contract.*?(\d+)\s*(?:month|months|mo)',
            r'duration.*?(\d+)\s*(?:month|months|mo)',
            r'term.*?(\d+)\s*(?:month|months|mo)'
        ]
        
        for pattern in tenure_patterns:
            match = re.search(pattern, jd_text)
            if match:
                tenure = int(match.group(1))
                # Convert to months if needed
                if 'year' in pattern or 'yr' in pattern:
                    tenure *= 12
                elif 'week' in pattern or 'wk' in pattern:
                    tenure = max(1, tenure // 4)  # Convert weeks to months (minimum 1)
                extracted_data['jd_tenure'] = tenure
                break
        
        # Enhanced experience requirements extraction
        exp_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:to|-)\s*(\d+(?:\.\d+)?)\s*(?:year|years|yr)',
            r'(\d+(?:\.\d+)?)\s*(?:year|years|yr).*?experience',
            r'experience.*?(\d+(?:\.\d+)?)\s*(?:year|years|yr)',
            r'(\d+(?:\.\d+)?)\s*(?:year|years|yr).*?minimum',
            r'minimum.*?(\d+(?:\.\d+)?)\s*(?:year|years|yr)',
            r'(\d+(?:\.\d+)?)\+?\s*(?:year|years|yr).*?experience',
            r'(\d+(?:\.\d+)?)\s*(?:year|years|yr).*?required'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, jd_text)
            if match:
                if 'to' in pattern or '-' in pattern:
                    extracted_data['jd_op_exp_min'] = float(match.group(1))
                    extracted_data['jd_op_exp_max'] = float(match.group(2))
                else:
                    min_exp = float(match.group(1))
                    extracted_data['jd_op_exp_min'] = min_exp
                    extracted_data['jd_op_exp_max'] = min_exp + 2  # Add 2 years as max
                break
        
        # Enhanced budget/salary information extraction
        # Note: Budget fields are NOT extracted automatically - they should be manually filled by HR
        # This prevents extracting salary information from JD text
        # extracted_data['jd_op_budget_min'] = None  # Manual input required
        # extracted_data['jd_op_budget_max'] = None  # Manual input required
        
        # Enhanced open positions extraction
        position_patterns = [
            r'(\d+)\s*(?:position|positions|role|roles|opening|openings)',
            r'(\d+)\s*(?:vacancy|vacancies|slot|slots)',
            r'looking.*?(\d+)\s*(?:candidate|candidates)',
            r'hiring.*?(\d+)\s*(?:developer|engineer|analyst)',
            r'(\d+)\s*(?:headcount|fte|full.?time)',
            r'team.*?(\d+)\s*(?:member|members)'
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, jd_text)
            if match:
                extracted_data['jd_open_position'] = int(match.group(1))
                # Set available positions to same as open positions initially
                extracted_data['jd_available_pos'] = str(match.group(1))
                break
        
        # Extract revenue potential based on budget and positions
        # Note: Since budget is now manual input, revenue potential will be calculated when budget is provided
        if 'jd_op_budget_max' in extracted_data and extracted_data['jd_op_budget_max'] and 'jd_open_position' in extracted_data and extracted_data['jd_open_position']:
            total_budget = extracted_data['jd_op_budget_max'] * extracted_data['jd_open_position']
            if total_budget > 500000:  # $500k+
                extracted_data['jd_revenue_potential'] = 'High'
            elif total_budget > 200000:  # $200k+
                extracted_data['jd_revenue_potential'] = 'Medium'
            else:
                extracted_data['jd_revenue_potential'] = 'Low'
        else:
            # Revenue potential will be calculated when budget is manually entered
            extracted_data['jd_revenue_potential'] = None
        
        # Enhanced keywords extraction (technical terms, tools, methodologies)
        keywords = []
        
        # Development Methodologies
        methodology_keywords = [
            'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd', 'tdd', 'bdd', 'ddd',
            'lean', 'six sigma', 'sprint', 'standup', 'retrospective', 'grooming', 'planning'
        ]
        
        # Architecture Patterns
        architecture_keywords = [
            'rest', 'graphql', 'soap', 'api', 'microservices', 'monolith', 'serverless',
            'event-driven', 'domain-driven', 'layered architecture', 'mvc', 'mvvm', 'clean architecture'
        ]
        
        # Testing & Quality
        testing_keywords = [
            'unit testing', 'integration testing', 'e2e testing', 'test automation', 'qa', 'quality assurance',
            'code review', 'pair programming', 'mob programming', 'code coverage', 'sonarqube'
        ]
        
        # Security & Performance
        security_keywords = [
            'oauth', 'jwt', 'ssl', 'tls', 'encryption', 'authentication', 'authorization',
            'penetration testing', 'vulnerability assessment', 'performance testing', 'load testing'
        ]
        
        # All keyword patterns combined
        keyword_patterns = methodology_keywords + architecture_keywords + testing_keywords + security_keywords
        
        for keyword in keyword_patterns:
            if keyword in jd_text:
                keywords.append(keyword)
        
        # Remove duplicates and limit
        extracted_data['jd_keywords'] = list(set(keywords))[:20]  # Increased limit for better coverage
        
        return jsonify({
            'success': True,
            'message': 'JD information extracted successfully',
            'data': extracted_data
        }), 200
        
    except Exception as e:
        print(f"Error scanning JD: {str(e)}")
        return jsonify({'error': f'Failed to scan JD: {str(e)}'}), 500

@app.route('/api/jd', methods=['POST'])
def create_job_description():
    """POST /api/jd - Create a new job description"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['jd_title', 'jd_original']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert job description into database
        cursor.execute('''
            INSERT INTO job_descriptions (
                jd_title, jd_customer_id, jd_consumer, jd_original, jd_skillset_cat,
                jd_skillset, jd_mode, jd_tenure, jd_op_exp_min, jd_op_exp_max,
                jd_op_budget_min, jd_op_budget_max, jd_open_position, jd_available_pos,
                jd_revenue_potential, jd_currency, jd_keywords, jd_source, jd_special_instruction,
                jd_created_by, jd_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('jd_title'),
            data.get('jd_customer_id'),
            data.get('jd_consumer'),
            data.get('jd_original'),
            data.get('jd_skillset_cat'),
            json.dumps(data.get('jd_skillset', [])) if isinstance(data.get('jd_skillset'), list) else data.get('jd_skillset'),
            data.get('jd_mode'),
            data.get('jd_tenure'),
            data.get('jd_op_exp_min'),
            data.get('jd_op_exp_max'),
            data.get('jd_op_budget_min'),
            data.get('jd_op_budget_max'),
            data.get('jd_open_position'),
            data.get('jd_available_pos'),
            data.get('jd_revenue_potential'),
            data.get('jd_currency', 'USD'),
            json.dumps(data.get('jd_keywords', [])) if isinstance(data.get('jd_keywords'), list) else data.get('jd_keywords'),
            data.get('jd_source'),
            data.get('jd_special_instruction'),
            data.get('jd_created_by'),
            data.get('jd_status', 1)
        ))
        
        jd_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Job Description created successfully!',
            'data': {'id': jd_id}
        }), 201
        
    except Exception as e:
        print(f"Error creating JD: {str(e)}")
        return jsonify({'error': f'Failed to create JD: {str(e)}'}), 500

@app.route('/api/jd', methods=['GET'])
def get_job_descriptions():
    """GET /api/jd - Get all job descriptions"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get job descriptions with related data
        cursor.execute('''
            SELECT 
                jd.*,
                c.customer_name,
                sc.category_name as skillset_category_name,
                em.mode_name as job_mode_name,
                s.status_name as job_status_name
            FROM job_descriptions jd
            LEFT JOIN customers c ON jd.jd_customer_id = c.customer_id
            LEFT JOIN skillset_categories sc ON jd.jd_skillset_cat = sc.category_id
            LEFT JOIN engagement_modes em ON jd.jd_mode = em.mode_id
            LEFT JOIN (
                SELECT 1 as status_id, 'Active' as status_name
                UNION SELECT 2, 'Draft'
                UNION SELECT 3, 'Closed'
            ) s ON jd.jd_status = s.status_id
            ORDER BY jd.jd_created_date DESC
        ''')
        
        rows = cursor.fetchall()
        job_descriptions = []
        
        for row in rows:
            job_desc = dict(row)
            # Parse JSON fields
            try:
                if job_desc['jd_skillset']:
                    job_desc['jd_skillset'] = json.loads(job_desc['jd_skillset'])
                if job_desc['jd_keywords']:
                    job_desc['jd_keywords'] = json.loads(job_desc['jd_keywords'])
            except:
                pass
            
            # Calculate aging if not set
            if not job_desc.get('jd_aging'):
                try:
                    created_date = datetime.fromisoformat(job_desc['jd_created_date'].replace('Z', '+00:00'))
                    current_date = datetime.now()
                    job_desc['jd_aging'] = (current_date - created_date).days
                except:
                    job_desc['jd_aging'] = 0
            
            job_descriptions.append(job_desc)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': job_descriptions
        }), 200
        
    except Exception as e:
        print(f"Error retrieving JDs: {str(e)}")
        return jsonify({'error': f'Failed to retrieve JDs: {str(e)}'}), 500

@app.route('/api/jd/<int:jd_id>', methods=['GET'])
def get_job_description(jd_id):
    """GET /api/jd/<id> - Get job description by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM job_descriptions WHERE jd_id = ?', (jd_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({'error': 'Job description not found'}), 404
        
        job_desc = dict(row)
        # Parse JSON fields
        try:
            if job_desc['jd_skillset']:
                job_desc['jd_skillset'] = json.loads(job_desc['jd_skillset'])
            if job_desc['jd_keywords']:
                job_desc['jd_keywords'] = json.loads(job_desc['jd_keywords'])
        except:
            pass
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': job_desc
        }), 200
        
    except Exception as e:
        print(f"Error retrieving JD: {str(e)}")
        return jsonify({'error': f'Failed to retrieve JD: {str(e)}'}), 500

@app.route('/api/jd/update-aging', methods=['POST'])
def update_aging():
    """POST /api/jd/update-aging - Update aging for all job descriptions"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all job descriptions
        cursor.execute('SELECT jd_id, jd_created_date FROM job_descriptions')
        jobs = cursor.fetchall()
        
        updated_count = 0
        for job in jobs:
            # Calculate aging in days
            created_date = datetime.fromisoformat(job['jd_created_date'].replace('Z', '+00:00'))
            current_date = datetime.now()
            aging_days = (current_date - created_date).days
            
            # Update aging in database
            cursor.execute('''
                UPDATE job_descriptions 
                SET jd_aging = ?, jd_updated_date = CURRENT_TIMESTAMP 
                WHERE jd_id = ?
            ''', (aging_days, job['jd_id']))
            updated_count += 1
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Aging updated for {updated_count} job descriptions',
            'updated_count': updated_count
        }), 200
        
    except Exception as e:
        print(f"Error updating aging: {str(e)}")
        return jsonify({'error': f'Failed to update aging: {str(e)}'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """GET /api/categories - Get all skillset categories"""
    categories = [
        {'category_id': 1, 'category_name': 'Frontend Development'},
        {'category_id': 2, 'category_name': 'Backend Development'},
        {'category_id': 3, 'category_name': 'Full Stack Development'},
        {'category_id': 4, 'category_name': 'DevOps'},
        {'category_id': 5, 'category_name': 'Data Science'},
        {'category_id': 6, 'category_name': 'Mobile Development'}
    ]
    return jsonify({'data': categories}), 200

@app.route('/api/modes', methods=['GET'])
def get_modes():
    """GET /api/modes - Get all job modes"""
    modes = [
        {'mode_id': 1, 'mode_name': 'Remote'},
        {'mode_id': 2, 'mode_name': 'Onsite'},
        {'mode_id': 3, 'mode_name': 'Hybrid'},
        {'mode_id': 4, 'mode_name': 'Contract'},
        {'mode_id': 5, 'mode_name': 'Part-time'}
    ]
    return jsonify({'data': modes}), 200

@app.route('/api/statuses', methods=['GET'])
def get_statuses():
    """GET /api/statuses - Get all job statuses"""
    statuses = [
        {'status_id': 1, 'status_name': 'Active'},
        {'status_id': 2, 'status_name': 'Draft'},
        {'status_id': 3, 'status_name': 'Closed'}
    ]
    return jsonify({'data': statuses}), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """GET /api/users - Get all users"""
    users = [
        {'user_id': 1, 'full_name': 'Nikitha'},
        {'user_id': 2, 'full_name': 'Gauthami'}
    ]
    return jsonify({'data': users}), 200

@app.route('/api/currencies', methods=['GET'])
def get_currencies():
    """GET /api/currencies - Get all available currencies"""
    currencies = [
        {'currency_code': 'USD', 'currency_name': 'US Dollar', 'symbol': '$'},
        {'currency_code': 'INR', 'currency_name': 'Indian Rupee', 'symbol': '₹'}
    ]
    return jsonify({'data': currencies}), 200

@app.route('/help', methods=['GET'])
def help_page():
    """Help page with contact information"""
    return jsonify({
        'title': 'Need Help?',
        'message': 'We\'re here to help you with the Job Description Management System',
        'contact': {
            'website': 'www.ankyahnexus.com',
            'description': 'Visit our website for support and more information',
            'support': 'For technical support or questions, please contact us through our website.'
        },
        'features': [
            'Scan and extract job description information automatically',
            'Manage job descriptions with comprehensive details',
            'Track skills, experience, and budget requirements',
            'Generate reports and analytics'
        ]
    }), 200

@app.route('/api/help', methods=['GET'])
def api_help():
    """API help endpoint for frontend integration"""
    return jsonify({
        'title': 'Help & Support',
        'contact': {
            'website': 'www.ankyahnexus.com',
            'email': 'support@ankyahnexus.com',
            'phone': '+1 (555) 123-4567'
        },
        'message': 'For assistance with the Job Description Management System, please visit our website or contact our support team.',
        'quick_links': [
            'User Guide',
            'FAQ',
            'Contact Support',
            'System Status'
        ]
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'jd-management-api',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Job Description Management API',
        'version': '1.0.0',
        'status': 'working',
        'endpoints': {
            'POST /api/jd/scan': 'Scan and extract JD information',
            'POST /api/jd': 'Create new job description',
            'GET /api/jd': 'Get all job descriptions',
            'GET /api/jd/<id>': 'Get job description by ID',
            'POST /api/jd/update-aging': 'Update aging for all job descriptions',
            'GET /api/categories': 'Get all skillset categories',
            'GET /api/modes': 'Get all job modes',
            'GET /api/statuses': 'Get all job statuses',
            'GET /api/users': 'Get all users',
            'GET /api/currencies': 'Get all available currencies',
            'GET /api/help': 'Get help and support information',
            'GET /help': 'Help page with contact details',
            'GET /health': 'Health check'
        }
    }), 200

if __name__ == '__main__':
    # Initialize database on startup
    init_database()
    
    print("🚀 Starting Clean Flask Backend Server...")
    print("📱 API available at: http://localhost:5000")
    print("🔌 Health check: http://localhost:5000/health")
    print("📚 API docs: http://localhost:5000/")
    print("🗄️ Database: SQLite (jd_database.db)")
    print("✨ Enhanced technical keyword extraction enabled!")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
