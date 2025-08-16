from flask import request, jsonify
from services.jd_service import JobDescriptionService
from utils.validators import validate_jd_data

class JobDescriptionController:
    """Controller for Job Description endpoints"""
    
    @staticmethod
    def create_jd():
        """Create a new job description"""
        try:
            # Get request data
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            
            # Validate data
            validation_result = validate_jd_data(data)
            if not validation_result['valid']:
                return jsonify({'success': False, 'error': validation_result['errors']}), 400
            
            # Create job description
            result = JobDescriptionService.create_jd(data)
            
            if result['success']:
                return jsonify(result), 201
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @staticmethod
    def get_jd(jd_id):
        """Get job description by ID"""
        try:
            result = JobDescriptionService.get_jd_by_id(jd_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @staticmethod
    def get_all_jds():
        """Get all job descriptions with pagination and search"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', None)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1 or per_page > 100:
                per_page = 10
            
            result = JobDescriptionService.get_all_jds(page=page, per_page=per_page, search=search)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @staticmethod
    def update_jd(jd_id):
        """Update an existing job description"""
        try:
            # Get request data
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': 'No data provided'}), 400
            
            # Validate data
            validation_result = validate_jd_data(data, is_update=True)
            if not validation_result['valid']:
                return jsonify({'success': False, 'error': validation_result['errors']}), 400
            
            # Update job description
            result = JobDescriptionService.update_jd(jd_id, data)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @staticmethod
    def delete_jd(jd_id):
        """Delete a job description"""
        try:
            result = JobDescriptionService.delete_jd(jd_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @staticmethod
    def search_jds():
        """Search job descriptions with advanced filters"""
        try:
            # Get search parameters
            search_params = {
                'mode': request.args.get('mode'),
                'primary_skill': request.args.get('primary_skill'),
                'experience_min': request.args.get('experience_min', type=float),
                'experience_max': request.args.get('experience_max', type=float),
                'budget_min': request.args.get('budget_min', type=float),
                'budget_max': request.args.get('budget_max', type=float),
                'tenure_min': request.args.get('tenure_min', type=int),
                'tenure_max': request.args.get('tenure_max', type=int),
                'search_text': request.args.get('search_text')
            }
            
            # Remove None values
            search_params = {k: v for k, v in search_params.items() if v is not None}
            
            result = JobDescriptionService.search_jds(search_params)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @staticmethod
    def get_statistics():
        """Get job description statistics"""
        try:
            result = JobDescriptionService.get_jd_statistics()
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Internal server error'}), 500 