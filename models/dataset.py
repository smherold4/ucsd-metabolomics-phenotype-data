# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Date, Integer, Numeric, Index, DateTime, ForeignKey, UniqueConstraint


class Dataset(base.Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    cohort_id = Column(Integer, ForeignKey('cohort.id'))
    units = Column(String, nullable=False, index=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        UniqueConstraint(
            "cohort_id",
            "units",
            name="uniq_cohort_units"),
    )

    UNITS = ['raw', 'normalized']

    cohort = relationship("Cohort", backref="datasets")

    @validates('units')
    def validate_units(self, key, value):
        assert value in Dataset.UNITS
        return value

    def __init__(self, cohort, units):
        self.cohort_id = cohort.id
        self.units = units
