"""Added new column.

Revision ID: c30cd032e39c
Revises: c657589b8c56
Create Date: 2023-05-27 15:07:29.792750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c30cd032e39c'
down_revision = 'c657589b8c56'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buildings', sa.Column('descript', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('buildings', 'descript')
    # ### end Alembic commands ###