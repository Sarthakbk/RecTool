-- Create database (if not exists)
CREATE DATABASE IF NOT EXISTS rectool_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE rectool_db;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(150) NOT NULL,
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_customer_code (customer_code),
    INDEX idx_customer_name (customer_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS skillset_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_category_name (category_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS engagement_modes (
    mode_id INT PRIMARY KEY AUTO_INCREMENT,
    mode_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_mode_name (mode_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'recruiter', 'manager', 'hr') NOT NULL DEFAULT 'recruiter',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS job_descriptions (
    jd_id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for each Job Description',
    jd_title VARCHAR(150) NOT NULL COMMENT 'Job Description Title',
    jd_customer_id INT NOT NULL COMMENT 'Customer Required Reference',
    jd_consumer VARCHAR(150) NOT NULL COMMENT 'Name of the Consumer',
    jd_original LONGTEXT NOT NULL COMMENT 'Original JD given by the Customer',
    jd_skillset_cat INT NOT NULL COMMENT 'Skillset category',
    jd_skillset JSON NOT NULL COMMENT 'Secondary skillsets',
    jd_mode INT NOT NULL COMMENT 'Engagement Mode',
    jd_tenure INT NOT NULL COMMENT 'Duration of the resource',
    jd_op_exp_min DECIMAL(4,1) NOT NULL COMMENT 'Operational Experience Min',
    jd_op_exp_max DECIMAL(4,1) NOT NULL COMMENT 'Operational Experience Max',
    jd_op_budget_min DECIMAL(10,2) NOT NULL COMMENT 'Budget Min',
    jd_op_budget_max DECIMAL(10,2) NOT NULL COMMENT 'Budget Max',
    jd_open_position INT NULL COMMENT 'No of positions',
    jd_available_pos VARCHAR(50) NULL COMMENT 'Available Positions',
    jd_revenue_potential VARCHAR(100) NULL COMMENT 'Revenue Potential',
    jd_keywords JSON NULL COMMENT 'Tech Keywords of JD',
    jd_aging INT GENERATED ALWAYS AS (DATEDIFF(CURDATE(), DATE(jd_created_date))) STORED COMMENT 'How old is this JD',
    jd_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Active status',
    jd_status VARCHAR(50) NOT NULL DEFAULT 'Open' COMMENT 'Shows the status of the JD',
    jd_created_by INT NOT NULL COMMENT 'HR or recruiter who entered the JD',
    jd_created_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Date of entry by HR or Recruiter',
    jd_updated_by INT NOT NULL COMMENT 'HR who updated the JD',
    jd_updated_date DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Date of entry by HR',
    jd_source LONGTEXT NULL COMMENT 'Source',
    jd_special_instruction LONGTEXT NULL COMMENT 'Attached of new job',
    
    -- Foreign key constraints
    FOREIGN KEY (jd_customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (jd_skillset_cat) REFERENCES skillset_categories(category_id) ON DELETE RESTRICT,
    FOREIGN KEY (jd_mode) REFERENCES engagement_modes(mode_id) ON DELETE RESTRICT,
    FOREIGN KEY (jd_created_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (jd_updated_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    
    -- Constraints
    CONSTRAINT chk_tenure_positive CHECK (jd_tenure > 0),
    CONSTRAINT chk_experience_range CHECK (jd_op_exp_min <= jd_op_exp_max),
    CONSTRAINT chk_budget_range CHECK (jd_op_budget_min <= jd_op_budget_max),
    CONSTRAINT chk_open_positions CHECK (jd_open_position IS NULL OR jd_open_position > 0),
    
    -- Indexes
    INDEX idx_title (jd_title),
    INDEX idx_customer (jd_customer_id),
    INDEX idx_consumer (jd_consumer),
    INDEX idx_skillset_cat (jd_skillset_cat),
    INDEX idx_mode (jd_mode),
    INDEX idx_tenure (jd_tenure),
    INDEX idx_experience_range (jd_op_exp_min, jd_op_exp_max),
    INDEX idx_budget_range (jd_op_budget_min, jd_op_budget_max),
    INDEX idx_status (jd_status),
    INDEX idx_active (jd_active),
    INDEX idx_created_date (jd_created_date),
    INDEX idx_aging (jd_aging),
    INDEX idx_created_by (jd_created_by),
    INDEX idx_updated_by (jd_updated_by),
    
    -- Full-text search indexes
    FULLTEXT idx_title_search (jd_title),
    FULLTEXT idx_consumer_search (jd_consumer),
    FULLTEXT idx_original_search (jd_original),
    FULLTEXT idx_keywords_search (jd_keywords),
    FULLTEXT idx_special_instruction_search (jd_special_instruction)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Job Status tracking table (enhanced)
-- =====================================================
CREATE TABLE IF NOT EXISTS job_status (
    status_id INT PRIMARY KEY AUTO_INCREMENT,
    jd_id INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    status_notes TEXT,
    changed_by INT NOT NULL,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jd_id) REFERENCES job_descriptions(jd_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    
    INDEX idx_jd_status (jd_id, status),
    INDEX idx_status_changed (status, changed_at),
    INDEX idx_changed_by (changed_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Sample data insertion
-- =====================================================

-- Insert sample customers
INSERT INTO customers (customer_name, customer_code) VALUES
('TechCorp Solutions', 'TCS001'),
('InnovateSoft Inc', 'ISI002'),
('Digital Dynamics', 'DD003');

-- Insert sample skillset categories
INSERT INTO skillset_categories (category_name, description) VALUES
('Frontend Development', 'Frontend technologies and frameworks'),
('Backend Development', 'Backend technologies and server-side development'),
('Full Stack Development', 'Both frontend and backend development'),
('DevOps', 'DevOps and infrastructure management'),
('Data Science', 'Data analysis and machine learning'),
('Mobile Development', 'Mobile app development');

-- Insert sample engagement modes
INSERT INTO engagement_modes (mode_name, description) VALUES
('Onsite', 'Work from client location'),
('Remote', 'Work from anywhere'),
('Hybrid', 'Combination of onsite and remote work'),
('Contract', 'Fixed-term contract work'),
('Full-time', 'Permanent full-time position');

-- Insert sample users
INSERT INTO users (username, email, full_name, role) VALUES
('admin', 'admin@rectool.com', 'System Administrator', 'admin'),
('hr1', 'hr1@rectool.com', 'Sarah Johnson', 'hr'),
('recruiter1', 'recruiter1@rectool.com', 'John Doe', 'recruiter'),
('manager1', 'manager1@rectool.com', 'Jane Smith', 'manager');

-- Sample job description
INSERT INTO job_descriptions (
    jd_title, 
    jd_customer_id,
    jd_consumer,
    jd_original,
    jd_skillset_cat,
    jd_skillset,
    jd_mode,
    jd_tenure,
    jd_op_exp_min,
    jd_op_exp_max,
    jd_op_budget_min,
    jd_op_budget_max,
    jd_open_position,
    jd_available_pos,
    jd_revenue_potential,
    jd_keywords,
    jd_status,
    jd_created_by,
    jd_updated_by,
    jd_special_instruction
) VALUES (
    'Senior React Developer',
    1,
    'TechCorp Solutions',
    'We are looking for a Senior React Developer to join our dynamic team. The ideal candidate will have strong experience in React development, state management, and modern JavaScript frameworks. Responsibilities include developing user-facing features, building reusable components, and collaborating with cross-functional teams.',
    1,
    '["NodeJS", "MySQL", "TypeScript", "Redux", "Next.js"]',
    3,
    12,
    3.0,
    5.0,
    60000.00,
    90000.00,
    5,
    '3',
    'High',
    '["React", "JavaScript", "Frontend", "UI/UX", "Component Development"]',
    'Open',
    2,
    2,
    'Candidate must be available to join within 30 days and willing to work in a hybrid environment.'
);

-- Insert initial status
INSERT INTO job_status (jd_id, status, changed_by) VALUES (1, 'Open', 2);

-- =====================================================
-- Views for common queries
-- =====================================================

-- Active job descriptions view
CREATE OR REPLACE VIEW v_active_jobs AS
SELECT 
    jd.jd_id,
    jd.jd_title,
    c.customer_name,
    jd.jd_consumer,
    sc.category_name as skillset_category,
    em.mode_name as engagement_mode,
    jd.jd_tenure,
    jd.jd_open_position,
    jd.jd_available_pos,
    jd.jd_op_exp_min,
    jd.jd_op_exp_max,
    jd.jd_op_budget_min,
    jd.jd_op_budget_max,
    jd.jd_status,
    jd.jd_aging,
    jd.jd_created_date,
    u.full_name as created_by
FROM job_descriptions jd
JOIN customers c ON jd.jd_customer_id = c.customer_id
JOIN skillset_categories sc ON jd.jd_skillset_cat = sc.category_id
JOIN engagement_modes em ON jd.jd_mode = em.mode_id
JOIN users u ON jd.jd_created_by = u.user_id
WHERE jd.jd_active = TRUE AND jd.jd_status IN ('Open', 'Active', 'On Hold');

-- Job summary statistics view
CREATE OR REPLACE VIEW v_job_summary AS
SELECT 
    COUNT(*) as total_jobs,
    COUNT(CASE WHEN jd.jd_active = TRUE THEN 1 END) as active_jobs,
    COUNT(CASE WHEN jd.jd_status = 'Open' THEN 1 END) as open_jobs,
    COUNT(CASE WHEN jd.jd_status = 'Closed' THEN 1 END) as closed_jobs,
    SUM(jd.jd_open_position) as total_open_positions,
    SUM(CAST(jd.jd_available_pos AS UNSIGNED)) as total_available_positions,
    AVG(jd.jd_tenure) as avg_tenure_months,
    AVG(jd.jd_op_budget_min) as avg_budget_min,
    AVG(jd.jd_op_budget_max) as avg_budget_max
FROM job_descriptions jd;

-- Customer job summary view
CREATE OR REPLACE VIEW v_customer_job_summary AS
SELECT 
    c.customer_name,
    COUNT(jd.jd_id) as total_jobs,
    COUNT(CASE WHEN jd.jd_active = TRUE THEN 1 END) as active_jobs,
    SUM(jd.jd_open_position) as total_positions,
    AVG(jd.jd_op_budget_min) as avg_budget_min,
    AVG(jd.jd_op_budget_max) as avg_budget_max
FROM customers c
LEFT JOIN job_descriptions jd ON c.customer_id = jd.jd_customer_id
GROUP BY c.customer_id, c.customer_name;

-- =====================================================
-- Stored procedures for common operations
-- =====================================================

DELIMITER //

-- Procedure to create a new job description
CREATE PROCEDURE sp_create_job_description(
    IN p_title VARCHAR(150),
    IN p_customer_id INT,
    IN p_consumer VARCHAR(150),
    IN p_original LONGTEXT,
    IN p_skillset_cat INT,
    IN p_skillset JSON,
    IN p_mode INT,
    IN p_tenure INT,
    IN p_exp_min DECIMAL(4,1),
    IN p_exp_max DECIMAL(4,1),
    IN p_budget_min DECIMAL(10,2),
    IN p_budget_max DECIMAL(10,2),
    IN p_open_positions INT,
    IN p_available_pos VARCHAR(50),
    IN p_revenue_potential VARCHAR(100),
    IN p_keywords JSON,
    IN p_status VARCHAR(50),
    IN p_created_by INT,
    IN p_special_instruction LONGTEXT
)
BEGIN
    DECLARE v_jd_id INT;
    
    -- Insert job description
    INSERT INTO job_descriptions (
        jd_title, jd_customer_id, jd_consumer, jd_original, jd_skillset_cat,
        jd_skillset, jd_mode, jd_tenure, jd_op_exp_min, jd_op_exp_max,
        jd_op_budget_min, jd_op_budget_max, jd_open_position, jd_available_pos,
        jd_revenue_potential, jd_keywords, jd_status, jd_created_by, 
        jd_updated_by, jd_special_instruction
    ) VALUES (
        p_title, p_customer_id, p_consumer, p_original, p_skillset_cat,
        p_skillset, p_mode, p_tenure, p_exp_min, p_exp_max,
        p_budget_min, p_budget_max, p_open_positions, p_available_pos,
        p_revenue_potential, p_keywords, p_status, p_created_by,
        p_created_by, p_special_instruction
    );
    
    SET v_jd_id = LAST_INSERT_ID();
    
    -- Insert initial status
    INSERT INTO job_status (jd_id, status, changed_by) VALUES (v_jd_id, p_status, p_created_by);
    
    SELECT v_jd_id as new_jd_id;
END //

-- Procedure to update job status
CREATE PROCEDURE sp_update_job_status(
    IN p_jd_id INT,
    IN p_status VARCHAR(50),
    IN p_notes TEXT,
    IN p_changed_by INT
)
BEGIN
    INSERT INTO job_status (jd_id, status, status_notes, changed_by)
    VALUES (p_jd_id, p_status, p_notes, p_changed_by);
    
    -- Update the main table status
    UPDATE job_descriptions SET jd_status = p_status, jd_updated_by = p_changed_by WHERE jd_id = p_jd_id;
    
    SELECT 'Status updated successfully' as message;
END //

-- Procedure to calculate JD aging
CREATE PROCEDURE sp_calculate_jd_aging()
BEGIN
    UPDATE job_descriptions 
    SET jd_aging = DATEDIFF(CURDATE(), DATE(jd_created_date))
    WHERE jd_active = TRUE;
    
    SELECT 'JD aging calculated successfully' as message;
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
    IF NEW.jd_open_position IS NOT NULL AND NEW.jd_available_pos IS NOT NULL THEN
        IF CAST(NEW.jd_available_pos AS UNSIGNED) > NEW.jd_open_position THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Available positions cannot exceed open positions';
        END IF;
    END IF;
END //

-- Trigger to log changes to job_descriptions
CREATE TRIGGER tr_log_jd_changes
AFTER UPDATE ON job_descriptions
FOR EACH ROW
BEGIN
    -- Update the updated_date automatically
    SET NEW.jd_updated_date = CURRENT_TIMESTAMP;
END //

-- Trigger to validate experience range
CREATE TRIGGER tr_validate_experience_range
BEFORE INSERT ON job_descriptions
FOR EACH ROW
BEGIN
    IF NEW.jd_op_exp_min > NEW.jd_op_exp_max THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Minimum experience cannot be greater than maximum experience';
    END IF;
END //

-- Trigger to validate budget range
CREATE TRIGGER tr_validate_budget_range
BEFORE INSERT ON job_descriptions
FOR EACH ROW
BEGIN
    IF NEW.jd_op_budget_min > NEW.jd_op_budget_max THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Minimum budget cannot be greater than maximum budget';
    END IF;
END //

DELIMITER ;

-- =====================================================
-- Comments and documentation
-- =====================================================

-- Add comments to table columns
ALTER TABLE job_descriptions 
MODIFY COLUMN jd_id INT COMMENT 'Unique identifier for each Job Description',
MODIFY COLUMN jd_title VARCHAR(150) COMMENT 'Job Description Title',
MODIFY COLUMN jd_customer_id INT COMMENT 'Customer Required Reference',
MODIFY COLUMN jd_consumer VARCHAR(150) COMMENT 'Name of the Consumer',
MODIFY COLUMN jd_original LONGTEXT COMMENT 'Original JD given by the Customer',
MODIFY COLUMN jd_skillset_cat INT COMMENT 'Skillset category',
MODIFY COLUMN jd_skillset JSON COMMENT 'Secondary skillsets',
MODIFY COLUMN jd_mode INT COMMENT 'Engagement Mode',
MODIFY COLUMN jd_tenure INT COMMENT 'Duration of the resource',
MODIFY COLUMN jd_op_exp_min DECIMAL(4,1) COMMENT 'Operational Experience Min',
MODIFY COLUMN jd_op_exp_max DECIMAL(4,1) COMMENT 'Operational Experience Max',
MODIFY COLUMN jd_op_budget_min DECIMAL(10,2) COMMENT 'Budget Min',
MODIFY COLUMN jd_op_budget_max DECIMAL(10,2) COMMENT 'Budget Max',
MODIFY COLUMN jd_open_position INT COMMENT 'No of positions',
MODIFY COLUMN jd_available_pos VARCHAR(50) COMMENT 'Available Positions',
MODIFY COLUMN jd_revenue_potential VARCHAR(100) COMMENT 'Revenue Potential',
MODIFY COLUMN jd_keywords JSON COMMENT 'Tech Keywords of JD',
MODIFY COLUMN jd_aging INT COMMENT 'How old is this JD',
MODIFY COLUMN jd_active BOOLEAN COMMENT 'Active status',
MODIFY COLUMN jd_status VARCHAR(50) COMMENT 'Shows the status of the JD',
MODIFY COLUMN jd_created_by INT COMMENT 'HR or recruiter who entered the JD',
MODIFY COLUMN jd_created_date DATETIME COMMENT 'Date of entry by HR or Recruiter',
MODIFY COLUMN jd_updated_by INT COMMENT 'HR who updated the JD',
MODIFY COLUMN jd_updated_date DATETIME COMMENT 'Date of entry by HR',
MODIFY COLUMN jd_source LONGTEXT COMMENT 'Source',
MODIFY COLUMN jd_special_instruction LONGTEXT COMMENT 'Attached of new job';

-- =====================================================
-- End of schema
-- ===================================================== 