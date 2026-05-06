-- Law Analyse Database Schema
-- Run this SQL script in Neon Console to create tables

-- Create enum type for processing status
CREATE TYPE processing_status AS ENUM ('pending', 'processing', 'completed', 'failed');

-- Create laws table
CREATE TABLE IF NOT EXISTS laws (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    document_number VARCHAR(100),
    publication_date TIMESTAMP,
    issuing_body VARCHAR(255),
    pdf_url TEXT,
    processing_status processing_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create articles table
CREATE TABLE IF NOT EXISTS articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    law_id UUID NOT NULL REFERENCES laws(id) ON DELETE CASCADE,
    article_number VARCHAR(50) NOT NULL,
    title TEXT,
    full_text TEXT NOT NULL,
    hierarchy_path TEXT[]
);

-- Create norms table
CREATE TABLE IF NOT EXISTS norms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    norm_type VARCHAR(50),
    norm_text TEXT NOT NULL,
    subject TEXT,
    simplified_explanation TEXT,
    confidence_score FLOAT NOT NULL,
    needs_human_review BOOLEAN NOT NULL DEFAULT FALSE,
    extraction_metadata JSONB
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_articles_law_id ON articles(law_id);
CREATE INDEX IF NOT EXISTS idx_norms_article_id ON norms(article_id);
CREATE INDEX IF NOT EXISTS idx_laws_status ON laws(processing_status);
CREATE INDEX IF NOT EXISTS idx_norms_review ON norms(needs_human_review);

-- Create alembic version table (for migration tracking)
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Insert initial version
INSERT INTO alembic_version (version_num) VALUES ('initial') ON CONFLICT DO NOTHING;
