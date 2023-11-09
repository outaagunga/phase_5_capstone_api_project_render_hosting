"""empty message

Revision ID: 330168ea7ae4
Revises: 558574a7a139
Create Date: 2023-11-09 02:01:34.690279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '330168ea7ae4'
down_revision = '558574a7a139'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nventory_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('item_name', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('item_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('date_to_warehouse', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.drop_column('inventory_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventory', schema=None) as batch_op:
        batch_op.add_column(sa.Column('inventory_id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('description')
        batch_op.drop_column('date_to_warehouse')
        batch_op.drop_column('quantity')
        batch_op.drop_column('item_type')
        batch_op.drop_column('item_name')
        batch_op.drop_column('nventory_id')

    # ### end Alembic commands ###