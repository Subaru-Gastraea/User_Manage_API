"""create user table

Revision ID: 1614da8c5ded
Revises: 
Create Date: 2023-01-07 11:22:59.831072

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '1614da8c5ded'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'userinfo_tb',
        sa.Column("username", sa.String, primary_key=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("birthday", sa.Date),
        sa.Column("create_time", sa.DateTime, default = datetime.utcnow()),
        sa.Column("last_login", sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('userinfo_tb')
