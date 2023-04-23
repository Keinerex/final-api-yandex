"""empty message

Revision ID: 422ebb1134e5
Revises: f3a734036eab
Create Date: 2023-04-22 22:20:32.829700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '422ebb1134e5'
down_revision = 'f3a734036eab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.VARCHAR(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('date')

    # ### end Alembic commands ###
