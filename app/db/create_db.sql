SELECT 'CREATE DATABASE clapdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'clapdb')\gexec