from flask import Blueprint
from controllers.jd_controller import JobDescriptionController

# Create blueprint for job description routes
jd_bp = Blueprint('job_descriptions', __name__, url_prefix='/api/jd')

# Route definitions
@jd_bp.route('/', methods=['POST'])
def create_jd():
    """Create a new job description"""
    return JobDescriptionController.create_jd()

@jd_bp.route('/<int:jd_id>', methods=['GET'])
def get_jd(jd_id):
    """Get job description by ID"""
    return JobDescriptionController.get_jd(jd_id)

@jd_bp.route('/', methods=['GET'])
def get_all_jds():
    """Get all job descriptions with pagination and search"""
    return JobDescriptionController.get_all_jds()

@jd_bp.route('/<int:jd_id>', methods=['PUT'])
def update_jd(jd_id):
    """Update an existing job description"""
    return JobDescriptionController.update_jd(jd_id)

@jd_bp.route('/<int:jd_id>', methods=['DELETE'])
def delete_jd(jd_id):
    """Delete a job description"""
    return JobDescriptionController.delete_jd(jd_id)

@jd_bp.route('/search', methods=['GET'])
def search_jds():
    """Search job descriptions with advanced filters"""
    return JobDescriptionController.search_jds()

@jd_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get job description statistics"""
    return JobDescriptionController.get_statistics()

# Health check endpoint
@jd_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'job-descriptions-api'}, 200 