"""Creating tables.

Revision ID: 12ee2543a4b9
Revises: 
Create Date: 2023-05-23 14:52:57.119346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12ee2543a4b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('buildings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('square', sa.String(), nullable=True),
    sa.Column('price', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fio', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('telegram', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('apps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client', sa.Integer(), nullable=True),
    sa.Column('building', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('ready', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['building'], ['buildings.id'], ),
    sa.ForeignKeyConstraint(['client'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
