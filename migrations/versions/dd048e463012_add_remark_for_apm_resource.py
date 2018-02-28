"""add remark for apm_resource

Revision ID: dd048e463012
Revises: c921dc1f3b2d
Create Date: 2018-01-31 11:44:25.951193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd048e463012'
down_revision = 'c921dc1f3b2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apm_resource', sa.Column('remark', sa.String(length=255), nullable=True))
    op.create_foreign_key(None, 'apm_resource', 'apm_user', ['apm_user_id'], ['apm_user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'apm_resource', type_='foreignkey')
    op.drop_column('apm_resource', 'remark')
    # ### end Alembic commands ###
