"""other models

Revision ID: 7d01a7e66b51
Revises: ee458ec34c78
Create Date: 2022-02-23 14:39:21.022378

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7d01a7e66b51'
down_revision = 'ee458ec34c78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
                    sa.Column('date_of_birth', sa.DateTime(), nullable=True),
                    sa.Column('personal_medical_history', sa.Text(), nullable=True),
                    sa.Column('family_medical_history', sa.Text(), nullable=True),
                    sa.Column('company_name', sa.Text(), nullable=True),
                    sa.Column('company_pib', sa.Integer(), nullable=True),
                    sa.Column('company_address', sa.String(), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('surname', sa.String(length=255), nullable=False),
                    sa.Column('jmbg', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('address', sa.String(length=255), nullable=True),
                    sa.Column('phone', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_of_creation', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('id'),
                    sa.UniqueConstraint('jmbg'),
                    sa.UniqueConstraint('phone')
                    )
    op.create_table('price_list',
                    sa.Column('services', sa.String(), nullable=True),
                    sa.Column('medical_service', sa.String(), nullable=True),
                    sa.Column('price_of_service', sa.Integer(), nullable=True),
                    sa.Column('time_for_exam', sa.Integer(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_of_creation', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('review_document',
                    sa.Column('url', sa.String(), nullable=True),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_of_creation', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('review',
                    sa.Column('customers_id', sa.Integer(), nullable=False),
                    sa.Column('doctor_id', sa.Integer(), nullable=False),
                    sa.Column('price_list_id', sa.Integer(), nullable=False),
                    sa.Column('price_of_service', sa.Integer(), nullable=True),
                    sa.Column('doctor_opinion', sa.Text(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_of_creation', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['customers_id'], ['customers.id'], ),
                    sa.ForeignKeyConstraint(['doctor_id'], ['user.id'], ),
                    sa.ForeignKeyConstraint(['price_list_id'], ['price_list.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('payments',
                    sa.Column('review_id', sa.Integer(), nullable=False),
                    sa.Column('customers_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('price_list_id', sa.Integer(), nullable=False),
                    sa.Column('price_of_service', sa.Integer(), nullable=False),
                    sa.Column('paid', sa.Boolean(), nullable=True),
                    sa.Column('payment_made', sa.Enum('cash', 'card', 'cash_card', name='pays'), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('date_of_creation', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['customers_id'], ['customers.id'], ),
                    sa.ForeignKeyConstraint(['price_list_id'], ['price_list.id'], ),
                    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_table('payments')
    op.drop_table('review')
    op.drop_table('review_document')
    op.drop_table('price_list')
    op.drop_table('customers')
    # ### end Alembic commands ###
