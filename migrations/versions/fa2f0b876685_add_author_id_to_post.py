"""Add author_id to post

Revision ID: fa2f0b876685
Revises: 
Create Date: 2025-05-22 14:07:42.977295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa2f0b876685'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add author_id column to post table with default value 1 (nullable=False)
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=False, server_default='1'))
        batch_op.create_foreign_key('fk_post_author_id', 'user', ['author_id'], ['id'])

    # Modify user table: add password_hash, drop password
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=False))
        batch_op.drop_column('password')


def downgrade():
    # Revert user table changes
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('password_hash')

    # Revert post table changes
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint('fk_post_author_id', type_='foreignkey')
        batch_op.drop_column('author_id')
