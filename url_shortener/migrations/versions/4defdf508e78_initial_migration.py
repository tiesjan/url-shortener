"""
Initial migration

Revision ID: 4defdf508e78
Revises: (none)
Create Date: 2021-10-19 20:14:59.350979
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4defdf508e78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'shortURL',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False),
        sa.Column('target_url', sa.String(length=500), nullable=False),
        sa.Column('public', sa.Boolean(), nullable=False),
        sa.Column('visit_count', sa.Integer(), server_default=sa.text('0'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )


def downgrade():
    op.drop_table('shortURL')
