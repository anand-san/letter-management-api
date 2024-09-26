ENABLE_UUID_EXTENSION = """CREATE EXTENSION IF NOT EXISTS "uuid-ossp";"""
USER_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        clerk_user_id VARCHAR(100) NOT NULL UNIQUE,
        clerk_metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    '''

DOCUMENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS documents (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        db_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        document_name VARCHAR(255) NOT NULL,
        document_path TEXT NOT NULL,
        document_type VARCHAR(50),
        size_in_bytes BIGINT,
        uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        metadata JSONB
    );
    """

DOCUMENTS_INDEXES = """CREATE INDEX IF NOT EXISTS idx_user_document 
ON documents (db_user_id, uploaded_at DESC);CREATE INDEX IF NOT EXISTS idx_document_type 
ON documents (document_type);CREATE INDEX IF NOT EXISTS gin_metadata_idx 
ON documents USING GIN (metadata);"""

# --- Create Index Separately ---
# CREATE INDEX idx_user_document ON documents(db_user_id, uploaded_at DESC);
# CREATE INDEX idx_document_type ON documents(document_type);
# CREATE INDEX gin_metadata_idx ON documents USING GIN (metadata);
