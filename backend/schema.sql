DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS brand_guidelines CASCADE;
DROP TABLE IF EXISTS content_posts CASCADE;

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
	file_analysis JSONB,
	analysis_generated_at TIMESTAMPTZ,
	voice TEXT,
	logos JSONB,
	typography TEXT,
	visual_style TEXT,
	content_rules TEXT,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
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
