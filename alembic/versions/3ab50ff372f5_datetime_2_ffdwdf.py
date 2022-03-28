"""datetime_2_ffdwdf

Revision ID: 3ab50ff372f5
Revises: 0c418a34fcb4
Create Date: 2022-03-28 11:52:52.582522

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ab50ff372f5'
down_revision = '0c418a34fcb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customers', 'date_of_birth',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('customers', 'date_of_birth',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
