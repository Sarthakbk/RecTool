from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class JobDescription(db.Model):
    """Job Description model"""
    __tablename__ = 'job_descriptions'
    
    jd_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jd_title = db.Column(db.String(150), nullable=False, index=True)
    primary_skill = db.Column(db.String(100), nullable=False, index=True)
    secondary_skills = db.Column(db.Text)
    mode = db.Column(db.Enum('Onsite', 'Remote', 'Hybrid'), nullable=False, index=True)
    tenure_months = db.Column(db.Integer, nullable=False)
    open_positions = db.Column(db.Integer, nullable=False)
    available_positions = db.Column(db.Integer, nullable=False)
    experience_min = db.Column(db.DECIMAL(4, 1))
    experience_max = db.Column(db.DECIMAL(4, 1))
    budget_min = db.Column(db.DECIMAL(10, 2))
    budget_max = db.Column(db.DECIMAL(10, 2))
    jd_keywords = db.Column(db.Text)
    original_jd = db.Column(db.LONGTEXT)
    special_instruction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<JobDescription {self.jd_title}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'jd_id': self.jd_id,
            'jd_title': self.jd_title,
            'primary_skill': self.primary_skill,
            'secondary_skills': self.secondary_skills,
            'mode': self.mode,
            'tenure_months': self.tenure_months,
            'open_positions': self.open_positions,
            'available_positions': self.available_positions,
            'experience_min': float(self.experience_min) if self.experience_min else None,
            'experience_max': float(self.experience_max) if self.experience_max else None,
            'budget_min': float(self.budget_min) if self.budget_min else None,
            'budget_max': float(self.budget_max) if self.budget_max else None,
            'jd_keywords': self.jd_keywords,
            'original_jd': self.original_jd,
            'special_instruction': self.special_instruction,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class JobDescriptionSchema(SQLAlchemyAutoSchema):
    """Marshmallow schema for JobDescription"""
    class Meta:
        model = JobDescription
        load_instance = True
        sqla_session = db.session
        include_fk = True

# Create schema instances
job_description_schema = JobDescriptionSchema()
job_descriptions_schema = JobDescriptionSchema(many=True) 