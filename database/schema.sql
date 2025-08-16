-- Create database (if not exists)
CREATE DATABASE IF NOT EXISTS rectool_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE rectool_db;

-- =====================================================
-- Users table (if you want to track who created/updated JDs)
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'recruiter', 'manager') NOT NULL DEFAULT 'recruiter',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Job Descriptions table
-- =====================================================
CREATE TABLE IF NOT EXISTS job_descriptions (
    jd_id INT PRIMARY KEY AUTO_INCREMENT,
    jd_title VARCHAR(150) NOT NULL,
    primary_skill VARCHAR(100) NOT NULL,
    secondary_skills TEXT,
    mode ENUM('Onsite', 'Remote', 'Hybrid') NOT NULL,
    tenure_months INT NOT NULL,
    open_positions INT NOT NULL,
    available_positions INT NOT NULL,
    experience_min DECIMAL(4,1) NULL,
    experience_max DECIMAL(4,1) NULL,
    budget_min DECIMAL(10,2) NULL,
    budget_max DECIMAL(10,2) NULL,
    jd_keywords TEXT,
    original_jd LONGTEXT,
    special_instruction TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign keys (optional - uncomment if users table exists)
    -- created_by INT NULL,
    -- updated_by INT NULL,
    
    -- Constraints
    CONSTRAINT chk_tenure_months CHECK (tenure_months > 0),
    CONSTRAINT chk_open_positions CHECK (open_positions > 0),
    CONSTRAINT chk_available_positions CHECK (available_positions >= 0),
    CONSTRAINT chk_experience_range CHECK (experience_min IS NULL OR experience_max IS NULL OR experience_min <= experience_max),
    CONSTRAINT chk_budget_range CHECK (budget_min IS NULL OR budget_max IS NULL OR budget_min <= budget_max),
    CONSTRAINT chk_available_vs_open CHECK (available_positions <= open_positions),
    
    -- Indexes
    INDEX idx_title (jd_title),
    INDEX idx_primary_skill (primary_skill),
    INDEX idx_mode (mode),
    INDEX idx_created_at (created_at),
    INDEX idx_experience_range (experience_min, experience_max),
    INDEX idx_budget_range (budget_min, budget_max),
    INDEX idx_tenure (tenure_months),
    INDEX idx_positions (open_positions, available_positions),
    
    -- Full-text search indexes
    FULLTEXT idx_title_search (jd_title),
    FULLTEXT idx_skills_search (primary_skill, secondary_skills),
    FULLTEXT idx_keywords_search (jd_keywords),
    FULLTEXT idx_original_jd_search (original_jd)
    
    -- Foreign key constraints (uncomment if users table exists)
    -- FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL,
    -- FOREIGN KEY (updated_by) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Job Status tracking table (optional enhancement)
-- =====================================================
CREATE TABLE IF NOT EXISTS job_status (
    status_id INT PRIMARY KEY AUTO_INCREMENT,
    jd_id INT NOT NULL,
    status ENUM('Draft', 'Active', 'On Hold', 'Closed', 'Archived') NOT NULL DEFAULT 'Draft',
    status_notes TEXT,
    changed_by INT NULL,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jd_id) REFERENCES job_descriptions(jd_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(user_id) ON DELETE SET NULL,
    
    INDEX idx_jd_status (jd_id, status),
    INDEX idx_status_changed (status, changed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Sample data insertion (optional)
-- =====================================================
INSERT INTO users (username, email, full_name, role) VALUES
('admin', 'admin@rectool.com', 'System Administrator', 'admin'),
('recruiter1', 'recruiter1@rectool.com', 'John Doe', 'recruiter'),
('manager1', 'manager1@rectool.com', 'Jane Smith', 'manager');

-- Sample job description
INSERT INTO job_descriptions (
    jd_title, 
    primary_skill, 
    secondary_skills, 
    mode, 
    tenure_months, 
    open_positions, 
    available_positions, 
    experience_min, 
    experience_max, 
    budget_min, 
    budget_max, 
    jd_keywords, 
    original_jd, 
    special_instruction
) VALUES (
    'Senior React Developer',
    'ReactJS',
    'NodeJS, MySQL, TypeScript, Redux',
    'Hybrid',
    12,
    5,
    3,
    3.0,
    5.0,
    60000.00,
    90000.00,
    'React, JavaScript, Frontend, UI/UX, Component Development',
    'We are looking for a Senior React Developer to join our dynamic team. The ideal candidate will have strong experience in React development, state management, and modern JavaScript frameworks. Responsibilities include developing user-facing features, building reusable components, and collaborating with cross-functional teams.',
    'Candidate must be available to join within 30 days and willing to work in a hybrid environment.'
);

-- =====================================================
-- Views for common queries
-- =====================================================

-- Active job descriptions view
CREATE OR REPLACE VIEW v_active_jobs AS
SELECT 
    jd.jd_id,
    jd.jd_title,
    jd.primary_skill,
    jd.mode,
    jd.tenure_months,
    jd.open_positions,
    jd.available_positions,
    jd.experience_min,
    jd.experience_max,
    jd.budget_min,
    jd.budget_max,
    jd.created_at,
    COALESCE(js.status, 'Draft') as current_status
FROM job_descriptions jd
LEFT JOIN job_status js ON jd.jd_id = js.jd_id 
    AND js.changed_at = (
        SELECT MAX(changed_at) 
        FROM job_status js2 
        WHERE js2.jd_id = jd.jd_id
    )
WHERE COALESCE(js.status, 'Draft') IN ('Draft', 'Active', 'On Hold');

-- Job summary statistics view
CREATE OR REPLACE VIEW v_job_summary AS
SELECT 
    COUNT(*) as total_jobs,
    COUNT(CASE WHEN mode = 'Remote' THEN 1 END) as remote_jobs,
    COUNT(CASE WHEN mode = 'Onsite' THEN 1 END) as onsite_jobs,
    COUNT(CASE WHEN mode = 'Hybrid' THEN 1 END) as hybrid_jobs,
    SUM(open_positions) as total_open_positions,
    SUM(available_positions) as total_available_positions,
    AVG(tenure_months) as avg_tenure_months
FROM job_descriptions;

-- =====================================================
-- Stored procedures for common operations
-- =====================================================

DELIMITER //

-- Procedure to create a new job description
CREATE PROCEDURE sp_create_job_description(
    IN p_title VARCHAR(150),
    IN p_primary_skill VARCHAR(100),
    IN p_secondary_skills TEXT,
    IN p_mode ENUM('Onsite', 'Remote', 'Hybrid'),
    IN p_tenure_months INT,
    IN p_open_positions INT,
    IN p_available_positions INT,
    IN p_experience_min DECIMAL(4,1),
    IN p_experience_max DECIMAL(4,1),
    IN p_budget_min DECIMAL(10,2),
    IN p_budget_max DECIMAL(10,2),
    IN p_jd_keywords TEXT,
    IN p_original_jd LONGTEXT,
    IN p_special_instruction TEXT,
    IN p_created_by INT
)
BEGIN
    DECLARE v_jd_id INT;
    
    -- Insert job description
    INSERT INTO job_descriptions (
        jd_title, primary_skill, secondary_skills, mode, tenure_months,
        open_positions, available_positions, experience_min, experience_max,
        budget_min, budget_max, jd_keywords, original_jd, special_instruction
    ) VALUES (
        p_title, p_primary_skill, p_secondary_skills, p_mode, p_tenure_months,
        p_open_positions, p_available_positions, p_experience_min, p_experience_max,
        p_budget_min, p_budget_max, p_jd_keywords, p_original_jd, p_special_instruction
    );
    
    SET v_jd_id = LAST_INSERT_ID();
    
    -- Insert initial status
    INSERT INTO job_status (jd_id, status, changed_by) VALUES (v_jd_id, 'Draft', p_created_by);
    
    SELECT v_jd_id as new_jd_id;
END //

-- Procedure to update job status
CREATE PROCEDURE sp_update_job_status(
    IN p_jd_id INT,
    IN p_status ENUM('Draft', 'Active', 'On Hold', 'Closed', 'Archived'),
    IN p_notes TEXT,
    IN p_changed_by INT
)
BEGIN
    INSERT INTO job_status (jd_id, status, status_notes, changed_by)
    VALUES (p_jd_id, p_status, p_notes, p_changed_by);
    
    SELECT 'Status updated successfully' as message;
END //

DELIMITER ;

-- =====================================================
-- Triggers for data integrity
-- =====================================================

DELIMITER //

-- Trigger to ensure available_positions doesn't exceed open_positions
CREATE TRIGGER tr_check_positions_before_update
BEFORE UPDATE ON job_descriptions
FOR EACH ROW
BEGIN
    IF NEW.available_positions > NEW.open_positions THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Available positions cannot exceed open positions';
    END IF;
END //

-- Trigger to log changes to job_descriptions
CREATE TRIGGER tr_log_jd_changes
AFTER UPDATE ON job_descriptions
FOR EACH ROW
BEGIN
    -- You can add logging logic here if needed
    -- For example, insert into an audit log table
END //

DELIMITER ;

-- =====================================================
-- Comments and documentation
-- =====================================================

-- Add comments to table columns
ALTER TABLE job_descriptions 
MODIFY COLUMN jd_id INT COMMENT 'Unique identifier for job description',
MODIFY COLUMN jd_title VARCHAR(150) COMMENT 'Job title/position name',
MODIFY COLUMN primary_skill VARCHAR(100) COMMENT 'Main required skill for the position',
MODIFY COLUMN secondary_skills TEXT COMMENT 'Additional skills that would be beneficial',
MODIFY COLUMN mode ENUM('Onsite', 'Remote', 'Hybrid') COMMENT 'Work location preference',
MODIFY COLUMN tenure_months INT COMMENT 'Contract duration in months',
MODIFY COLUMN open_positions INT COMMENT 'Total number of positions to fill',
MODIFY COLUMN available_positions INT COMMENT 'Number of positions currently available',
MODIFY COLUMN experience_min DECIMAL(4,1) COMMENT 'Minimum years of experience required',
MODIFY COLUMN experience_max DECIMAL(4,1) COMMENT 'Maximum years of experience preferred',
MODIFY COLUMN budget_min DECIMAL(10,2) COMMENT 'Minimum budget/salary for the position',
MODIFY COLUMN budget_max DECIMAL(10,2) COMMENT 'Maximum budget/salary for the position',
MODIFY COLUMN jd_keywords TEXT COMMENT 'Searchable keywords for the position',
MODIFY COLUMN original_jd LONGTEXT COMMENT 'Original job description text from customer',
MODIFY COLUMN special_instruction TEXT COMMENT 'Special requirements or instructions';

-- =====================================================
-- End of schema
-- ===================================================== 