"""phone_unique=False_add

Revision ID: 0bf817568b0d
Revises: df417257ae2c
Create Date: 2022-03-04 15:53:49.528943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bf817568b0d'
down_revision = 'df417257ae2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('customers_phone_key', 'customers', type_='unique')
    op.drop_constraint('user_phone_key', 'user', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_phone_key', 'user', ['phone'])
    op.create_unique_constraint('customers_phone_key', 'customers', ['phone'])
    # ### end Alembic commands ###
