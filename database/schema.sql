-- DKS Digital Pet System Database Schema

-- Pet States Table
CREATE TABLE pet_states (
    pet_id VARCHAR(36) PRIMARY KEY,
    owner_id VARCHAR(36) NULL,
    pet_name VARCHAR(100) NULL,
    traits JSON NOT NULL,
    trait_connections JSON NOT NULL,
    vital_stats JSON NOT NULL,
    needs JSON NOT NULL,
    memory JSON NOT NULL,
    behavior_patterns JSON NOT NULL,
    attention_level FLOAT DEFAULT 50.0,
    development_stage VARCHAR(20) DEFAULT 'infant',
    age FLOAT DEFAULT 0.0,
    position_x FLOAT DEFAULT 0,
    position_y FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_owner_id (owner_id),
    INDEX idx_development_stage (development_stage),
    INDEX idx_last_updated (last_updated)
);

-- Interactions Table
CREATE TABLE pet_interactions (
    interaction_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NULL,
    pet_id VARCHAR(36) NOT NULL,
    interaction_type VARCHAR(50) NOT NULL, -- feed, play, pet, train, check
    content JSON NOT NULL,
    mood_impact FLOAT DEFAULT 0,
    relationship_impact FLOAT DEFAULT 0,
    attention_impact FLOAT DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_pet (user_id, pet_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_interaction_type (interaction_type),
    FOREIGN KEY (pet_id) REFERENCES pet_states(pet_id) ON DELETE CASCADE
);

-- Simulation Runs Table
CREATE TABLE pet_environments (
    environment_id VARCHAR(36) PRIMARY KEY,
    environment_name VARCHAR(100) NOT NULL,
    environment_type VARCHAR(50) NOT NULL, -- standard, custom, event, etc.
    parameters JSON NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    status VARCHAR(20) DEFAULT 'active',
    environment_metrics JSON NULL,
    INDEX idx_environment_type (environment_type),
    INDEX idx_start_time (start_time)
);

-- Pet Metrics Table
CREATE TABLE pet_metrics (
    metric_id VARCHAR(36) PRIMARY KEY,
    pet_id VARCHAR(36) NOT NULL,
    environment_id VARCHAR(36) NOT NULL,
    time_step INT NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    additional_data JSON NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pet_step (pet_id, time_step),
    INDEX idx_environment_step (environment_id, time_step),
    INDEX idx_metric_type (metric_type),
    FOREIGN KEY (pet_id) REFERENCES pet_states(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (environment_id) REFERENCES pet_environments(environment_id) ON DELETE CASCADE
);

-- Relationships Table (for network visualization)
CREATE TABLE pet_relationships (
    relationship_id VARCHAR(36) PRIMARY KEY,
    environment_id VARCHAR(36) NOT NULL,
    entity_a_id VARCHAR(36) NOT NULL,
    entity_a_type ENUM('pet', 'user') NOT NULL,
    entity_b_id VARCHAR(36) NOT NULL,
    entity_b_type ENUM('pet', 'user') NOT NULL,
    relationship_strength FLOAT DEFAULT 0,
    relationship_quality VARCHAR(50) NULL, -- friendly, hostile, neutral, etc.
    interaction_count INT DEFAULT 0,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_environment_entities (environment_id, entity_a_id, entity_b_id),
    INDEX idx_relationship_strength (relationship_strength),
    FOREIGN KEY (environment_id) REFERENCES pet_environments(environment_id) ON DELETE CASCADE
);

-- User Table
CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_preferences JSON NULL,
    token_balance BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Tokens Table (for optional token economy)
CREATE TABLE tokens (
    transaction_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- mint, transfer, burn, reward, etc.
    amount BIGINT NOT NULL,
    recipient_id VARCHAR(36) NULL,
    related_pet_id VARCHAR(36) NULL,
    transaction_data JSON NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_timestamp (timestamp),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Initialize with default environment data
INSERT INTO pet_environments (environment_id, environment_name, environment_type, parameters, status) 
VALUES (
    'default-environment-001', 
    'Default Pet World', 
    'standard', 
    '{"num_pets": 5, "grid_width": 20, "grid_height": 20, "ambient_energy": 1.0, "social_atmosphere": 0.7}',
    'active'
);
