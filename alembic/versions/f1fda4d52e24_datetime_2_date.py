"""datetime_2_date

Revision ID: f1fda4d52e24
Revises: b3ee7d1a3f0a
Create Date: 2022-03-28 10:30:29.498461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f1fda4d52e24'
down_revision = 'b3ee7d1a3f0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customers', 'date_of_birth')
    op.drop_column('price_list', 'date_of_end')
    op.drop_column('review', 'date_of_creation_payment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('date_of_creation_payment', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('price_list', sa.Column('date_of_end', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('customers', sa.Column('date_of_birth', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###