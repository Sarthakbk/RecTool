#!/usr/bin/env python3
"""
MySQL-based HTTP Server for JD Management System
This server uses Flask with MySQL database
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import configuration
from mysql_config import get_database_url, SETUP_INSTRUCTIONS

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import Flask app and database
from backend.models.job_description import db, JobDescription

# Create Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize database
db.init_app(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize database
with app.app_context():
    try:
        db.create_all()
        print("✅ MySQL database tables created successfully!")
        
        # Check if sample data exists
        existing_jd = JobDescription.query.first()
        if not existing_jd:
            # Create sample data
            sample_jd = JobDescription(
                jd_title='Senior React Developer',
                primary_skill='ReactJS',
                secondary_skills='NodeJS, MySQL, TypeScript',
                mode='Hybrid',
                tenure_months=12,
                open_positions=5,
                available_positions=3,
                experience_min=3.0,
                experience_max=5.0,
                budget_min=60000.00,
                budget_max=90000.00,
                jd_keywords='React, JavaScript, Frontend',
                original_jd='We are looking for a Senior React Developer to join our dynamic team.',
                special_instruction='Candidate must join within 30 days.'
            )
            db.session.add(sample_jd)
            db.session.commit()
            print("✅ Sample data inserted successfully!")
        else:
            print("✅ Sample data already exists!")
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        print("\n" + "="*60)
        print("🔧 SETUP REQUIRED:")
        print("="*60)
        print(SETUP_INSTRUCTIONS)
        print("="*60)
        print(f"❌ Error: {e}")
        print("Make sure MySQL is running and the database is created!")
        print("Run the SQL script 'setup_mysql_database.sql' in MySQL Workbench first.")

@app.route('/api/jd/', methods=['POST'])
def create_jd():
    """Create a new job description"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['jd_title', 'primary_skill', 'mode', 'tenure_months', 'open_positions']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # Create new job description
        new_jd = JobDescription(
            jd_title=data.get('jd_title'),
            primary_skill=data.get('primary_skill'),
            secondary_skills=data.get('secondary_skills', ''),
            mode=data.get('mode'),
            tenure_months=int(data.get('tenure_months')),
            open_positions=int(data.get('open_positions')),
            available_positions=int(data.get('available_positions', 0)),
            experience_min=float(data.get('experience_min')) if data.get('experience_min') else None,
            experience_max=float(data.get('experience_max')) if data.get('experience_max') else None,
            budget_min=float(data.get('budget_min')) if data.get('budget_min') else None,
            budget_max=float(data.get('budget_max')) if data.get('budget_max') else None,
            jd_keywords=data.get('jd_keywords', ''),
            original_jd=data.get('original_jd', ''),
            special_instruction=data.get('special_instruction', '')
        )
        
        db.session.add(new_jd)
        db.session.commit()
        
        print(f"✅ New JD saved to MySQL: {new_jd.jd_title} (ID: {new_jd.jd_id})")
        
        return jsonify({
            'success': True,
            'data': {'jd_id': new_jd.jd_id},
            'message': 'Job description created successfully and saved to MySQL database!'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error saving to MySQL: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jd/', methods=['GET'])
def get_all_jds():
    """Get all job descriptions with pagination and search"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search = request.args.get('search', '')
        
        query = JobDescription.query
        
        if search:
            query = query.filter(
                db.or_(
                    JobDescription.jd_title.like(f'%{search}%'),
                    JobDescription.primary_skill.like(f'%{search}%'),
                    JobDescription.jd_keywords.like(f'%{search}%')
                )
            )
        
        # Get paginated results
        pagination = query.order_by(JobDescription.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        jds_list = []
        for jd in pagination.items:
            jds_list.append({
                'jd_id': jd.jd_id,
                'jd_title': jd.jd_title,
                'primary_skill': jd.primary_skill,
                'secondary_skills': jd.secondary_skills,
                'mode': jd.mode,
                'tenure_months': jd.tenure_months,
                'open_positions': jd.open_positions,
                'available_positions': jd.available_positions,
                'experience_min': jd.experience_min,
                'experience_max': jd.experience_max,
                'budget_min': jd.budget_min,
                'budget_max': jd.budget_max,
                'jd_keywords': jd.jd_keywords,
                'original_jd': jd.original_jd,
                'special_instruction': jd.special_instruction,
                'created_at': jd.created_at.isoformat() if jd.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': jds_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jd/<int:jd_id>', methods=['GET'])
def get_jd_by_id(jd_id):
    """Get job description by ID"""
    try:
        jd = JobDescription.query.get(jd_id)
        
        if not jd:
            return jsonify({'success': False, 'error': 'Job description not found'}), 404
        
        jd_dict = {
            'jd_id': jd.jd_id,
            'jd_title': jd.jd_title,
            'primary_skill': jd.primary_skill,
            'secondary_skills': jd.secondary_skills,
            'mode': jd.mode,
            'tenure_months': jd.tenure_months,
            'open_positions': jd.open_positions,
            'available_positions': jd.available_positions,
            'experience_min': jd.experience_min,
            'experience_max': jd.experience_max,
            'budget_min': jd.budget_min,
            'budget_max': jd.budget_max,
            'jd_keywords': jd.jd_keywords,
            'original_jd': jd.original_jd,
            'special_instruction': jd.special_instruction,
            'created_at': jd.created_at.isoformat() if jd.created_at else None
        }
        
        return jsonify({'success': True, 'data': jd_dict})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jd/statistics', methods=['GET'])
def get_statistics():
    """Get job description statistics"""
    try:
        # Total jobs
        total_jobs = JobDescription.query.count()
        
        # Jobs by mode
        mode_stats = db.session.query(
            JobDescription.mode, 
            db.func.count(JobDescription.jd_id)
        ).group_by(JobDescription.mode).all()
        
        mode_counts = dict(mode_stats)
        
        # Total positions
        positions = db.session.query(
            db.func.sum(JobDescription.open_positions),
            db.func.sum(JobDescription.available_positions)
        ).first()
        
        total_open = positions[0] or 0
        total_available = positions[1] or 0
        
        # Average tenure
        avg_tenure = db.session.query(
            db.func.avg(JobDescription.tenure_months)
        ).scalar() or 0
        
        stats = {
            'total_jobs': total_jobs,
            'remote_jobs': mode_counts.get('Remote', 0),
            'onsite_jobs': mode_counts.get('Onsite', 0),
            'hybrid_jobs': mode_counts.get('Hybrid', 0),
            'total_open_positions': total_open,
            'total_available_positions': total_available,
            'avg_tenure_months': round(avg_tenure, 1)
        }
        
        return jsonify({'success': True, 'data': stats})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception as e:
        db_status = f'disconnected: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'service': 'jd-management-api',
        'database': db_status,
        'database_type': 'MySQL',
        'database_name': 'rectool_db',
        'table_name': 'job_descriptions'
    })

if __name__ == '__main__':
    print("🚀 MySQL-based JD Management Server starting...")
    print("📱 Frontend: http://localhost:3000")
    print("🔌 API: http://localhost:5000/api/")
    print("💚 Health: http://localhost:5000/health")
    print("🗄️  Database: MySQL (rectool_db.job_descriptions)")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
