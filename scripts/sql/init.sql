CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(128) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS knowledge_files (
    file_id VARCHAR(64) PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL,
    object_key VARCHAR(255) NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    file_size INT NOT NULL,
    upload_time VARCHAR(64) NOT NULL,
    uploader VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_health_risk_assessment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    user_name VARCHAR(128) NOT NULL,
    sex VARCHAR(16) NOT NULL,
    age INT NOT NULL,
    assessment_time VARCHAR(64) NOT NULL,
    assessment_count INT DEFAULT 1,
    total_score INT NOT NULL,
    nutritional_impairment_score INT NOT NULL,
    disease_severity_score INT NOT NULL,
    age_score INT NOT NULL,
    assessment_basis TEXT NOT NULL,
    risk_level VARCHAR(32) NOT NULL,
    recommendations TEXT NOT NULL,
    bmi VARCHAR(32),
    weight_change VARCHAR(64),
    disease_condition VARCHAR(255),
    dietary_intake VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE PROCEDURE AddAssessmentRecord(
    IN p_user_id INT,
    IN p_user_name VARCHAR(128),
    IN p_sex VARCHAR(16),
    IN p_age INT,
    IN p_total_score INT,
    IN p_nutrition_score INT,
    IN p_disease_score INT,
    IN p_age_score INT,
    IN p_assessment_basis TEXT,
    IN p_recommendations TEXT
)
BEGIN
    DECLARE p_risk_level VARCHAR(32);
    IF p_total_score >= 3 THEN
        SET p_risk_level = 'high';
    ELSE
        SET p_risk_level = 'low';
    END IF;

    INSERT INTO user_health_risk_assessment (
        user_id, user_name, sex, age, assessment_time, assessment_count,
        total_score, nutritional_impairment_score, disease_severity_score, age_score,
        assessment_basis, risk_level, recommendations
    ) VALUES (
        p_user_id, p_user_name, p_sex, p_age, NOW(), 1,
        p_total_score, p_nutrition_score, p_disease_score, p_age_score,
        p_assessment_basis, p_risk_level, p_recommendations
    );
END$$
DELIMITER ;

CREATE OR REPLACE VIEW high_risk_patients AS
SELECT * FROM user_health_risk_assessment WHERE total_score >= 3;

CREATE OR REPLACE VIEW latest_assessments AS
SELECT a.* FROM user_health_risk_assessment a
JOIN (
    SELECT user_id, MAX(assessment_time) AS latest_time
    FROM user_health_risk_assessment
    GROUP BY user_id
) b ON a.user_id = b.user_id AND a.assessment_time = b.latest_time;
