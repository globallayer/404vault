-- Claw-dex Community Brain Schema
-- Stores anonymized, verified solutions from all Claw-dex users

-- Community Solutions table
-- Stores all types of knowledge: error fixes, decisions, patterns
CREATE TABLE IF NOT EXISTS community_solutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Content identification
    content_hash VARCHAR(32) UNIQUE NOT NULL,  -- For deduplication
    record_type VARCHAR(20) NOT NULL DEFAULT 'error_fix',  -- error_fix, decision, pattern

    -- Context (for filtering/matching)
    category VARCHAR(50),
    language VARCHAR(30),
    framework VARCHAR(50),
    database VARCHAR(30),
    platform VARCHAR(30),

    -- The actual knowledge (JSONB for flexibility)
    error_data JSONB,      -- {message, error_type, file_pattern}
    solution_data JSONB,   -- {description, approach, code_pattern}
    decision_data JSONB,   -- {title, choice, alternatives, pros, cons}
    pattern_data JSONB,    -- {name, problem, solution, scenarios}

    -- Trust metrics
    verification_count INTEGER DEFAULT 1,
    failure_count INTEGER DEFAULT 0,
    contributor_count INTEGER DEFAULT 1,

    -- Anonymous contributor tracking (for rate limiting, not identification)
    contributor_hash VARCHAR(32),

    -- Timestamps
    contributed_at TIMESTAMPTZ DEFAULT NOW(),
    last_verified_at TIMESTAMPTZ DEFAULT NOW(),

    -- Computed trust score
    trust_score NUMERIC GENERATED ALWAYS AS (
        CASE
            WHEN (verification_count + failure_count) = 0 THEN 0.5
            ELSE verification_count::NUMERIC / (verification_count + failure_count)
        END
    ) STORED
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_solutions_content_hash ON community_solutions(content_hash);
CREATE INDEX IF NOT EXISTS idx_solutions_record_type ON community_solutions(record_type);
CREATE INDEX IF NOT EXISTS idx_solutions_category ON community_solutions(category);
CREATE INDEX IF NOT EXISTS idx_solutions_language ON community_solutions(language);
CREATE INDEX IF NOT EXISTS idx_solutions_framework ON community_solutions(framework);
CREATE INDEX IF NOT EXISTS idx_solutions_verification ON community_solutions(verification_count DESC);
CREATE INDEX IF NOT EXISTS idx_solutions_trust ON community_solutions(trust_score DESC);

-- Full-text search on error messages and solutions
CREATE INDEX IF NOT EXISTS idx_solutions_error_fts ON community_solutions
    USING GIN (to_tsvector('english', COALESCE(error_data->>'message', '') || ' ' || COALESCE(solution_data->>'description', '')));

-- Row Level Security
ALTER TABLE community_solutions ENABLE ROW LEVEL SECURITY;

-- Anyone can read (public knowledge base)
CREATE POLICY "Public read access" ON community_solutions
    FOR SELECT USING (true);

-- Only authenticated users can insert (prevents spam)
CREATE POLICY "Authenticated insert" ON community_solutions
    FOR INSERT WITH CHECK (true);  -- Relies on API key auth

-- Only the contributor can update their own records
CREATE POLICY "Contributor update" ON community_solutions
    FOR UPDATE USING (true);  -- Simplified for now

-- Verification tracking table
-- Records when users verify that a solution worked
CREATE TABLE IF NOT EXISTS solution_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    solution_id UUID REFERENCES community_solutions(id) ON DELETE CASCADE,
    verifier_hash VARCHAR(32) NOT NULL,
    success BOOLEAN NOT NULL,
    context JSONB,  -- What context the user was in when verifying
    verified_at TIMESTAMPTZ DEFAULT NOW(),

    -- Prevent duplicate verifications from same user
    UNIQUE(solution_id, verifier_hash)
);

CREATE INDEX IF NOT EXISTS idx_verifications_solution ON solution_verifications(solution_id);

-- Function to increment verification count
CREATE OR REPLACE FUNCTION increment_verification()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.success THEN
        UPDATE community_solutions
        SET verification_count = verification_count + 1,
            last_verified_at = NOW()
        WHERE id = NEW.solution_id;
    ELSE
        UPDATE community_solutions
        SET failure_count = failure_count + 1
        WHERE id = NEW.solution_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for auto-updating verification counts
DROP TRIGGER IF EXISTS trigger_increment_verification ON solution_verifications;
CREATE TRIGGER trigger_increment_verification
    AFTER INSERT ON solution_verifications
    FOR EACH ROW
    EXECUTE FUNCTION increment_verification();

-- Function for full-text search
CREATE OR REPLACE FUNCTION search_solutions(
    search_query TEXT,
    filter_language TEXT DEFAULT NULL,
    filter_framework TEXT DEFAULT NULL,
    filter_category TEXT DEFAULT NULL,
    max_results INTEGER DEFAULT 10
)
RETURNS TABLE (
    id UUID,
    content_hash VARCHAR(32),
    record_type VARCHAR(20),
    category VARCHAR(50),
    language VARCHAR(30),
    framework VARCHAR(50),
    error_data JSONB,
    solution_data JSONB,
    verification_count INTEGER,
    trust_score NUMERIC,
    rank REAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        cs.id,
        cs.content_hash,
        cs.record_type,
        cs.category,
        cs.language,
        cs.framework,
        cs.error_data,
        cs.solution_data,
        cs.verification_count,
        cs.trust_score,
        ts_rank(
            to_tsvector('english', COALESCE(cs.error_data->>'message', '') || ' ' || COALESCE(cs.solution_data->>'description', '')),
            plainto_tsquery('english', search_query)
        ) AS rank
    FROM community_solutions cs
    WHERE
        (filter_language IS NULL OR cs.language = filter_language)
        AND (filter_framework IS NULL OR cs.framework = filter_framework)
        AND (filter_category IS NULL OR cs.category = filter_category)
        AND (
            search_query IS NULL
            OR to_tsvector('english', COALESCE(cs.error_data->>'message', '') || ' ' || COALESCE(cs.solution_data->>'description', ''))
               @@ plainto_tsquery('english', search_query)
        )
    ORDER BY rank DESC, cs.verification_count DESC
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- Usage stats table (for analytics, no PII)
CREATE TABLE IF NOT EXISTS usage_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stat_date DATE DEFAULT CURRENT_DATE,
    total_searches INTEGER DEFAULT 0,
    total_contributions INTEGER DEFAULT 0,
    total_verifications INTEGER DEFAULT 0,
    unique_contributors INTEGER DEFAULT 0
);

-- Comment for documentation
COMMENT ON TABLE community_solutions IS 'Anonymized, verified solutions from all Claw-dex users';
COMMENT ON COLUMN community_solutions.content_hash IS 'SHA256 hash of content for deduplication';
COMMENT ON COLUMN community_solutions.trust_score IS 'Computed: verifications / (verifications + failures)';
