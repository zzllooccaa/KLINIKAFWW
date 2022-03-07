"""added_foreign_key_Finance_id

Revision ID: 20a19c461157
Revises: b3b573f46568
Create Date: 2022-03-07 14:31:57.285814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20a19c461157'
down_revision = 'b3b573f46568'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('finance_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'review', 'user', ['finance_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'review', type_='foreignkey')
    op.drop_column('review', 'finance_id')
    # ### end Alembic commands ###
