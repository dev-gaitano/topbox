DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS brand_guidelines CASCADE;
DROP TABLE IF EXISTS content_posts CASCADE;

CREATE TABLE users (
	id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
	username VARCHAR(30) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX idx_users_username_lower ON users (LOWER(username));
CREATE UNIQUE INDEX idx_users_email_lower ON users (LOWER(email));

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    user_agent TEXT,
    ip_address INET
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_refresh_token_hash ON sessions(refresh_token_hash);

CREATE TABLE IF NOT EXISTS companies (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	logo TEXT DEFAULT '',
	industry TEXT DEFAULT '',
	email VARCHAR(255) UNIQUE,
	description TEXT DEFAULT '',
	target_audience TEXT DEFAULT '',
	color_palette JSONB DEFAULT '[]',
	unique_value TEXT DEFAULT '',
	main_competitors JSONB DEFAULT '[]',
	personality JSONB DEFAULT '[]',
	tone TEXT DEFAULT '',
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS brand_playbooks (
	id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
	company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
	file_path TEXT,
	file_uploaded_at TIMESTAMPTZ,
	file_saved_at TIMESTAMPTZ,
	text_extracted TEXT,
	file_analysis JSONB,
	analysis_generated_at TIMESTAMPTZ,
	voice TEXT,
	logos JSONB,
	typography_direction TEXT,
	headline_typeface TEXT,
	body_typeface TEXT,
	accent_typeface TEXT,
	visual_style TEXT,
	content_rules TEXT,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	UNIQUE (company_id)
);

CREATE TABLE IF NOT EXISTS content_posts (
	id SERIAL PRIMARY KEY,
	company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
	topic TEXT NOT NULL,
	platform TEXT NOT NULL,
	reference_image_urls JSONB,
	prompt TEXT,
	caption TEXT,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMPTZ
);
