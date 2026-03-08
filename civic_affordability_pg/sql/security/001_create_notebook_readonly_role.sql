-- Create a read-only login role for notebook users.
-- Replace placeholders before manual execution:
--   {{ROLE_NAME}}
--   {{ROLE_PASSWORD}}

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{{ROLE_NAME}}') THEN
    EXECUTE format('CREATE ROLE %I LOGIN PASSWORD %L', '{{ROLE_NAME}}', '{{ROLE_PASSWORD}}');
  ELSE
    EXECUTE format('ALTER ROLE %I WITH LOGIN PASSWORD %L', '{{ROLE_NAME}}', '{{ROLE_PASSWORD}}');
  END IF;
END $$;
