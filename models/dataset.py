# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Date, Integer, Numeric, Index, DateTime, ForeignKey, UniqueConstraint


class Dataset(base.Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True)
    cohort_id = Column(Integer, ForeignKey('cohort.id'))
    method = Column(String, nullable=False, index=True)
    units = Column(String, nullable=False, index=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        UniqueConstraint(
            "cohort_id",
            "method",
            "units",
            name="uniq_cohort_method_units"),
    )

    METHODS = ['LCMS', 'Eicosanoid']
    UNITS = ['raw', 'normalized']

    cohort = relationship("Cohort", backref="datasets")

    @validates('method')
    def validate_method(self, key, value):
        assert value in Dataset.METHODS
        return value

    @validates('units')
    def validate_units(self, key, value):
        assert value in Dataset.UNITS
        return value

    def __init__(self, cohort, method, units):
        self.cohort_id = cohort.id
        self.method = method
        self.units = units

    def source(self):
        return 'plasma'
