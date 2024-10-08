"""remove row

Revision ID: e054ee175ce3
Revises: d71ca70c82e3
Create Date: 2024-09-12 13:13:33.155733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e054ee175ce3'
down_revision: Union[str, None] = 'd71ca70c82e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'test')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('test', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
