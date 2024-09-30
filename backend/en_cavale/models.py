from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from en_cavale import db


class Country(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50))
    arrival: so.Mapped[sa.Date] = so.mapped_column(sa.Date)
    departure: so.Mapped[sa.Date] = so.mapped_column(sa.Date)
    region: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))

    def __repr__(self):
        return "<Country {} from the {} to the{}>".format(
            self.name, self.arrival, self.departure
        )


class Category(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50))

    def __repr__(self):
        return "<Category {}>".format(self.name)


class Spending(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[sa.Date] = so.mapped_column(sa.Date)
    amount: so.Mapped[sa.DECIMAL] = so.mapped_column(sa.DECIMAL(10, 2))
    currency: so.Mapped[str] = so.mapped_column(sa.String(3), server_default="CAD")
    category_id: so.Mapped[Optional[int]] = so.mapped_column(
        sa.Integer, sa.ForeignKey("category.id")
    )
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)

    def __repr__(self):
        return "<Spending {} on {} for {} {}, {}>".format(
            self.date, self.category_id, self.amount, self.currency, self.description
        )
