"""add service and svc_res_rel table

Revision ID: 310c2d57bec7
Revises: 8b846b156d6f
Create Date: 2018-01-31 15:46:23.370356

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '310c2d57bec7'
down_revision = '8b846b156d6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apm_service',
    sa.Column('apm_service_id', sa.Integer(), nullable=False),
    sa.Column('apm_service_name', sa.String(length=128), nullable=True),
    sa.Column('status', sa.String(length=8), nullable=True),
    sa.Column('apm_user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apm_user_id'], ['apm_user.apm_user_id'], ),
    sa.PrimaryKeyConstraint('apm_service_id')
    )
    op.create_table('apm_svc_res_rel',
    sa.Column('apm_svc_res_rel_id', sa.Integer(), nullable=False),
    sa.Column('apm_service_id', sa.Integer(), nullable=True),
    sa.Column('apm_resource_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['apm_resource_id'], ['apm_resource.apm_resource_id'], ),
    sa.ForeignKeyConstraint(['apm_service_id'], ['apm_service.apm_service_id'], ),
    sa.PrimaryKeyConstraint('apm_svc_res_rel_id')
    )
    op.create_foreign_key(None, 'apm_resource', 'apm_user', ['apm_user_id'], ['apm_user_id'])
    op.drop_column('apm_resource', 'remark')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apm_resource', sa.Column('remark', mysql.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'apm_resource', type_='foreignkey')
    op.drop_table('apm_svc_res_rel')
    op.drop_table('apm_service')
    # ### end Alembic commands ###
