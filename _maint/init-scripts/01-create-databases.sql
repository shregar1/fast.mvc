-- =============================================================================
-- FastX DataI Initialization
-- =============================================================================
-- This script runs automatically when PostgreSQL container starts for the first time
-- =============================================================================

-- Create test database
CREATE DATABASE fastmvc_test;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE fastx TO postgres;
GRANT ALL PRIVILEGES ON DATABASE fastmvc_test TO postgres;

-- Create extensions
\c fastx;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

\c fastmvc_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
