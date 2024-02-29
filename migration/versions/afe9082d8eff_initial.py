"""initial

Revision ID: afe9082d8eff
Revises: 
Create Date: 2024-01-08 00:13:25.142201

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afe9082d8eff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_telegram_id', sa.Integer(), nullable=False),
                    sa.Column('bucket', sa.String(length=255), nullable=False),
                    sa.Column('file_path', sa.String(length=255), nullable=False),
                    sa.Column('image_id', sa.String(length=255), nullable=False),
                    sa.Column('file_unique_id', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('file_unique_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
