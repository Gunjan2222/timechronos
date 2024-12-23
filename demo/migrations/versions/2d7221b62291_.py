"""empty message

Revision ID: 2d7221b62291
Revises: 4ac19ee4b99e
Create Date: 2024-10-24 18:11:56.745347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d7221b62291'
down_revision = '4ac19ee4b99e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('taskhours', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comments', sa.ARRAY(sa.String()), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('taskhours', schema=None) as batch_op:
        batch_op.drop_column('comments')

    # ### end Alembic commands ###
