"""Add background fields to users table

Revision ID: 001
Revises:
Create Date: 2025-12-25 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime

# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add software_background and hardware_background columns to users table
    op.add_column('user', sa.Column('software_background', sa.String(200), nullable=False, server_default=''))
    op.add_column('user', sa.Column('hardware_background', sa.String(200), nullable=False, server_default=''))

    # Update the server_default values to remove empty strings for new users
    # This will require a separate migration or direct SQL in a real scenario
    # For now, we'll just add the columns with nullable=False and empty defaults


def downgrade() -> None:
    # Remove software_background and hardware_background columns from users table
    op.drop_column('user', 'software_background')
    op.drop_column('user', 'hardware_background')