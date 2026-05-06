"""Initial migration - create laws, articles, norms tables

Revision ID: 001_initial
Revises:
Create Date: 2026-05-06 14:31:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create enum type for processing status (skip if exists)
    from sqlalchemy import inspect
    conn = op.get_bind()
    inspector = inspect(conn)

    # Check if enum type exists
    result = conn.execute(sa.text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'processingstatus')"))
    enum_exists = result.scalar()

    if not enum_exists:
        processing_status = postgresql.ENUM('pending', 'processing', 'completed', 'failed', name='processingstatus')
        processing_status.create(conn, checkfirst=True)

    # Use existing enum type
    processing_status = postgresql.ENUM('pending', 'processing', 'completed', 'failed', name='processingstatus', create_type=False)

    # Create laws table
    op.create_table(
        'laws',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('document_number', sa.String(length=100), nullable=True),
        sa.Column('publication_date', sa.DateTime(), nullable=True),
        sa.Column('issuing_body', sa.String(length=255), nullable=True),
        sa.Column('pdf_url', sa.Text(), nullable=True),
        sa.Column('processing_status', processing_status, nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('NOW()')),
    )

    # Create articles table
    op.create_table(
        'articles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('law_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('article_number', sa.String(length=50), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('full_text', sa.Text(), nullable=False),
        sa.Column('hierarchy_path', postgresql.ARRAY(sa.String()), nullable=True),
        sa.ForeignKeyConstraint(['law_id'], ['laws.id'], ondelete='CASCADE'),
    )

    # Create norms table
    op.create_table(
        'norms',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('norm_type', sa.String(length=50), nullable=True),
        sa.Column('norm_text', sa.Text(), nullable=False),
        sa.Column('subject', sa.Text(), nullable=True),
        sa.Column('simplified_explanation', sa.Text(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('needs_human_review', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('extraction_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
    )

    # Create indexes
    op.create_index('idx_articles_law_id', 'articles', ['law_id'])
    op.create_index('idx_norms_article_id', 'norms', ['article_id'])
    op.create_index('idx_laws_status', 'laws', ['processing_status'])
    op.create_index('idx_norms_review', 'norms', ['needs_human_review'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_norms_review', table_name='norms')
    op.drop_index('idx_laws_status', table_name='laws')
    op.drop_index('idx_norms_article_id', table_name='norms')
    op.drop_index('idx_articles_law_id', table_name='articles')

    # Drop tables
    op.drop_table('norms')
    op.drop_table('articles')
    op.drop_table('laws')

    # Drop enum
    sa.Enum(name='processingstatus').drop(op.get_bind(), checkfirst=True)
