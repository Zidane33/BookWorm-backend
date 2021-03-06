"""empty message

Revision ID: 261eed6be125
Revises: 
Create Date: 2020-01-01 10:49:42.349970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '261eed6be125'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('author', sa.String(length=120), nullable=True))
    op.add_column('books', sa.Column('title', sa.String(length=120), nullable=True))
    op.create_index(op.f('ix_books_author'), 'books', ['author'], unique=False)
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_index(op.f('ix_books_author'), table_name='books')
    op.drop_column('books', 'title')
    op.drop_column('books', 'author')
    # ### end Alembic commands ###
