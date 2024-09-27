"""seed initial data

Revision ID: 9d54be5c0995
Revises: b1e892b046ae
Create Date: 2024-09-27 08:22:12.935368

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9d54be5c0995"
down_revision = "b1e892b046ae"
branch_labels = None
depends_on = None

# Table definition (used only for the migration)
category_table = sa.Table(
    "category",
    sa.MetaData(),
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(50), nullable=False),
)


def upgrade():
    # Insert initial seed data
    op.bulk_insert(
        category_table,
        [
            {"name": "Hébergement"},
            {"name": "Visite"},
            {"name": "Course"},
            {"name": "Snack"},
            {"name": "Transport"},
            {"name": "Restaurant"},
        ],
    )


def downgrade():
    # Optionally delete the seed data on downgrade
    op.execute(
        "DELETE FROM category WHERE name IN ('Hébergement', 'Visite', 'Course', 'Snack', 'Transport', 'Restaurant')"
    )
