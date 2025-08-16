from typing import List, Optional, Dict, Any
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, and_
from models.job_description import db, JobDescription, job_description_schema, job_descriptions_schema

class JobDescriptionService:
    """Service class for Job Description operations"""
    
    @staticmethod
    def create_jd(jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job description"""
        try:
            # Validate required fields
            required_fields = ['jd_title', 'primary_skill', 'mode', 'tenure_months', 'open_positions']
            for field in required_fields:
                if not jd_data.get(field):
                    return {'success': False, 'error': f'Missing required field: {field}'}
            
            # Create new job description
            new_jd = JobDescription(**jd_data)
            db.session.add(new_jd)
            db.session.commit()
            
            # Return created job description
            result = job_description_schema.dump(new_jd)
            return {'success': True, 'data': result}
            
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error creating JD: {str(e)}")
            return {'success': False, 'error': 'Database error occurred'}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating JD: {str(e)}")
            return {'success': False, 'error': 'An error occurred while creating job description'}
    
    @staticmethod
    def get_jd_by_id(jd_id: int) -> Dict[str, Any]:
        """Get job description by ID"""
        try:
            jd = JobDescription.query.get(jd_id)
            if not jd:
                return {'success': False, 'error': 'Job description not found'}
            
            result = job_description_schema.dump(jd)
            return {'success': True, 'data': result}
            
        except Exception as e:
            current_app.logger.error(f"Error retrieving JD {jd_id}: {str(e)}")
            return {'success': False, 'error': 'An error occurred while retrieving job description'}
    
    @staticmethod
    def get_all_jds(page: int = 1, per_page: int = 10, search: Optional[str] = None) -> Dict[str, Any]:
        """Get all job descriptions with pagination and search"""
        try:
            query = JobDescription.query
            
            # Apply search filter if provided
            if search:
                search_filter = or_(
                    JobDescription.jd_title.ilike(f'%{search}%'),
                    JobDescription.primary_skill.ilike(f'%{search}%'),
                    JobDescription.jd_keywords.ilike(f'%{search}%'),
                    JobDescription.original_jd.ilike(f'%{search}%')
                )
                query = query.filter(search_filter)
            
            # Apply pagination
            pagination = query.order_by(JobDescription.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            # Serialize results
            jds = job_descriptions_schema.dump(pagination.items)
            
            return {
                'success': True,
                'data': jds,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
            
        except Exception as e:
            current_app.logger.error(f"Error retrieving JDs: {str(e)}")
            return {'success': False, 'error': 'An error occurred while retrieving job descriptions'}
    
    @staticmethod
    def update_jd(jd_id: int, jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing job description"""
        try:
            jd = JobDescription.query.get(jd_id)
            if not jd:
                return {'success': False, 'error': 'Job description not found'}
            
            # Update fields
            for key, value in jd_data.items():
                if hasattr(jd, key):
                    setattr(jd, key, value)
            
            db.session.commit()
            
            # Return updated job description
            result = job_description_schema.dump(jd)
            return {'success': True, 'data': result}
            
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error updating JD {jd_id}: {str(e)}")
            return {'success': False, 'error': 'Database error occurred'}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating JD {jd_id}: {str(e)}")
            return {'success': False, 'error': 'An error occurred while updating job description'}
    
    @staticmethod
    def delete_jd(jd_id: int) -> Dict[str, Any]:
        """Delete a job description"""
        try:
            jd = JobDescription.query.get(jd_id)
            if not jd:
                return {'success': False, 'error': 'Job description not found'}
            
            db.session.delete(jd)
            db.session.commit()
            
            return {'success': True, 'message': 'Job description deleted successfully'}
            
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error deleting JD {jd_id}: {str(e)}")
            return {'success': False, 'error': 'Database error occurred'}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting JD {jd_id}: {str(e)}")
            return {'success': False, 'error': 'An error occurred while deleting job description'}
    
    @staticmethod
    def search_jds(search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced search for job descriptions"""
        try:
            query = JobDescription.query
            
            # Apply filters
            if search_params.get('mode'):
                query = query.filter(JobDescription.mode == search_params['mode'])
            
            if search_params.get('primary_skill'):
                query = query.filter(JobDescription.primary_skill.ilike(f"%{search_params['primary_skill']}%"))
            
            if search_params.get('experience_min') is not None:
                query = query.filter(JobDescription.experience_max >= search_params['experience_min'])
            
            if search_params.get('experience_max') is not None:
                query = query.filter(JobDescription.experience_min <= search_params['experience_max'])
            
            if search_params.get('budget_min') is not None:
                query = query.filter(JobDescription.budget_max >= search_params['budget_min'])
            
            if search_params.get('budget_max') is not None:
                query = query.filter(JobDescription.budget_min <= search_params['budget_max'])
            
            if search_params.get('tenure_min'):
                query = query.filter(JobDescription.tenure_months >= search_params['tenure_min'])
            
            if search_params.get('tenure_max'):
                query = query.filter(JobDescription.tenure_months <= search_params['tenure_max'])
            
            # Apply search text
            if search_params.get('search_text'):
                search_filter = or_(
                    JobDescription.jd_title.ilike(f'%{search_params["search_text"]}%'),
                    JobDescription.jd_keywords.ilike(f'%{search_params["search_text"]}%'),
                    JobDescription.original_jd.ilike(f'%{search_params["search_text"]}%')
                )
                query = query.filter(search_filter)
            
            # Execute query
            jds = query.order_by(JobDescription.created_at.desc()).all()
            result = job_descriptions_schema.dump(jds)
            
            return {'success': True, 'data': result, 'count': len(result)}
            
        except Exception as e:
            current_app.logger.error(f"Error searching JDs: {str(e)}")
            return {'success': False, 'error': 'An error occurred while searching job descriptions'}
    
    @staticmethod
    def get_jd_statistics() -> Dict[str, Any]:
        """Get job description statistics"""
        try:
            total_jds = JobDescription.query.count()
            remote_jds = JobDescription.query.filter_by(mode='Remote').count()
            onsite_jds = JobDescription.query.filter_by(mode='Onsite').count()
            hybrid_jds = JobDescription.query.filter_by(mode='Hybrid').count()
            
            # Calculate total positions
            total_open = db.session.query(db.func.sum(JobDescription.open_positions)).scalar() or 0
            total_available = db.session.query(db.func.sum(JobDescription.available_positions)).scalar() or 0
            
            # Average tenure
            avg_tenure = db.session.query(db.func.avg(JobDescription.tenure_months)).scalar() or 0
            
            return {
                'success': True,
                'data': {
                    'total_jobs': total_jds,
                    'remote_jobs': remote_jds,
                    'onsite_jobs': onsite_jds,
                    'hybrid_jobs': hybrid_jds,
                    'total_open_positions': int(total_open),
                    'total_available_positions': int(total_available),
                    'avg_tenure_months': round(float(avg_tenure), 1) if avg_tenure else 0
                }
            }
            
        except Exception as e:
            current_app.logger.error(f"Error getting JD statistics: {str(e)}")
            return {'success': False, 'error': 'An error occurred while retrieving statistics'} 