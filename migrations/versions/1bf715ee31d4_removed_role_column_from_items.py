"""Removed role column from items

Revision ID: 1bf715ee31d4
Revises: 38aa930ebfde
Create Date: 2015-11-21 15:42:46.098251

"""

# revision identifiers, used by Alembic.
revision = '1bf715ee31d4'
down_revision = '38aa930ebfde'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'items_role_id_fkey', 'items', type_='foreignkey')
    op.drop_column('items', 'role_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'items_role_id_fkey', 'items', 'roles', ['role_id'], ['id'])
    ### end Alembic commands ###
