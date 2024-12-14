"""empty message

Revision ID: 31c8ba5138dd
Revises: ca8ef4a670f9
Create Date: 2024-10-25 14:36:05.600107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31c8ba5138dd'
down_revision = 'ca8ef4a670f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('taskhours', schema=None) as batch_op:
        batch_op.add_column(sa.Column('billable_type', sa.Enum('BILLABLE', 'NON_BILLABLE', 'BOTH', name='billabletype'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('taskhours', schema=None) as batch_op:
        batch_op.drop_column('billable_type')

    # ### end Alembic commands ###
