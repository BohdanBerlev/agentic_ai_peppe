-- Common database baseline for the course.
-- Application-specific tables and the actual RAG schema are team work.
CREATE EXTENSION IF NOT EXISTS vector;

-- Work Items Tabelle für den internen Dry Run
CREATE TABLE IF NOT EXISTS work_items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);