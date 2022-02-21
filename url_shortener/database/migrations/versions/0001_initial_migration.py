"""
Initial migration

Revision ID: 4defdf508e78
Revises: (none)
Create Date: 2021-10-19 20:14:59.350979
"""

from alembic import op
import sqlalchemy as sa

from url_shortener.database.functions import utc_now


# revision identifiers, used by Alembic.
revision = '4defdf508e78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create ShortURL table
    op.create_table(
        'short_url',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('target_url', sa.String(length=500), nullable=False),
        sa.Column('public', sa.Boolean(), nullable=False),
        sa.Column('visit_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=utc_now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )


def downgrade():
    # Drop ShortURL table
    op.drop_table(
        'short_url'
    )
