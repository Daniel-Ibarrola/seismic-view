"""Email model

Revision ID: 6af57abe0d0b
Revises: 6b4334eed8cd
Create Date: 2024-02-17 20:30:02.485296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6af57abe0d0b'
down_revision = '6b4334eed8cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('emails', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_emails_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('emails', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_emails_email'))

    op.drop_table('emails')
    # ### end Alembic commands ###
