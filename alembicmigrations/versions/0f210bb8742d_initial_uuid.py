"""initial UUID

Revision ID: 0f210bb8742d
Revises: 
Create Date: 2024-01-13 19:33:59.342974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '0f210bb8742d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    def create_users_table():
        op.create_table('admins',
        sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('admin_name', sa.String(length=50), nullable=False),
        sa.Column('permissions', sa.String(length=20), server_default='superadmin', nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('admin_id')
        )
        op.create_table('features',
        sa.Column('amenity_id', sa.Integer(), nullable=False),
        sa.Column('amenity_name', sa.String(length=50), nullable=True),
        sa.Column('amenity_plan_name', sa.String(length=50), nullable=True),
        sa.Column('amenity_for', sa.String(length=50), nullable=True),
        sa.Column('is_paid', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('amenity_id')
        )
        op.create_table('pincode_master',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('pincode', sa.Integer(), nullable=False),
        sa.Column('city', sa.String(length=35), nullable=True),
        sa.Column('district', sa.String(length=25), nullable=True),
        sa.Column('state', sa.String(length=15), nullable=True),
        sa.PrimaryKeyConstraint('id')
        )
        op.create_table('notice_board',
            sa.Column('notice_id', sa.VARCHAR(length=36), nullable=False),
            sa.Column('content', sa.String(length=2000), nullable=False),
            sa.Column('user_id', sa.VARCHAR(length=36), nullable=True),
            sa.Column('last_updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.PrimaryKeyConstraint('notice_id'),
            sa.UniqueConstraint('notice_id')
        )

        op.create_table('society_wings_details',
            sa.Column('society_id', sa.Integer(), nullable=False),
            sa.Column('wing_id', sa.Integer(), nullable=False),
            sa.Column('wing_name', sa.String(length=50), nullable=False),
            sa.Column('amenity_plan_name', sa.String(length=50), nullable=True),
            sa.Column('notice_id', sa.VARCHAR(length=36), nullable=True),
            sa.PrimaryKeyConstraint('wing_id')
        )

        op.create_table('users',
            sa.Column('user_id', sa.VARCHAR(length=36), nullable=False),
            sa.Column('phone', sa.String(length=15), nullable=True),
            sa.Column('user_type', sa.String(length=20), nullable=True),
            sa.Column('device_token', sa.String(length=255), nullable=True),
            sa.Column('name', sa.String(length=50), nullable=True),
            sa.Column('on_duty', sa.Boolean(), nullable=True),
            sa.Column('status', sa.Boolean(), nullable=True),
            sa.Column('society_id', sa.Integer(), nullable=True),
            sa.Column('wing_id', sa.Integer(), nullable=True),
            sa.PrimaryKeyConstraint('user_id'),
            sa.UniqueConstraint('user_id')
        )

        op.create_table('SOS',
            sa.Column('pincode_master_id', sa.Integer(), nullable=False),
            sa.Column('SOS_details', sa.JSON(), nullable=False),
            sa.PrimaryKeyConstraint('pincode_master_id')
        )

        op.create_table('society',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('society_name', sa.String(length=255), nullable=False),
            sa.Column('pincode_master_id', sa.Integer(), nullable=False),
            sa.Column('address', sa.Text(), nullable=False),
            sa.Column('latitude', sa.Float(), nullable=False),
            sa.Column('longitude', sa.Float(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )

        op.create_table('user_features',
            sa.Column('user_id', mysql.VARCHAR(length=36), nullable=False),
            sa.Column('amenity_id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('user_id', 'amenity_id')
        )

        op.create_table('user_features_association',
            sa.Column('user_id', mysql.VARCHAR(length=36), nullable=False),
            sa.Column('amenity_id', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('user_id', 'amenity_id')
        )
       

    def add_foreign_keys():
        op.create_foreign_key('fk_notice_board_user_id', 'notice_board', 'users', ['user_id'], ['user_id'])
        op.create_foreign_key('fk_society_wings_details_notice_id', 'society_wings_details', 'notice_board', ['notice_id'], ['notice_id'])
        op.create_foreign_key('fk_society_wings_details_society_id', 'society_wings_details', 'society', ['society_id'], ['id'])
        op.create_foreign_key('fk_users_society_id', 'users', 'society', ['society_id'], ['id'])
        op.create_foreign_key('fk_users_wing_id', 'users', 'society_wings_details', ['wing_id'], ['wing_id'])
        op.create_foreign_key('fk_sos_pincode_master_id', 'SOS', 'pincode_master', ['pincode_master_id'], ['id'])
        op.create_foreign_key('fk_society_pincode_master_id', 'society', 'pincode_master', ['pincode_master_id'], ['id'])
        op.create_foreign_key('fk_user_features_association_user_id', 'user_features_association', 'users', ['user_id'], ['user_id'])
        op.create_foreign_key('fk_user_features_association_amenity_id', 'user_features_association', 'features', ['amenity_id'], ['amenity_id'])  
        op.create_foreign_key('fk_user_features_amenity_id', 'user_features', 'features', ['amenity_id'], ['amenity_id'])
        op.create_foreign_key('fk_user_features_user_id', 'user_features', 'users', ['user_id'], ['user_id'])
        
         
    # create_users_table()
    add_foreign_keys()

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_features_association')
    op.drop_table('user_features')
    op.drop_table('society')
    op.drop_table('SOS')
    op.drop_table('users')
    op.drop_table('society_wings_details')
    op.drop_table('pincode_master')
    op.drop_table('notice_board')
    op.drop_table('features')
    op.drop_table('admins')
    # ### end Alembic commands ###
