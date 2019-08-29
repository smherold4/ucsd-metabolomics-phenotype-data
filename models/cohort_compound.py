# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Text, Date, Integer, Numeric, Index, DateTime, ForeignKey, UniqueConstraint


class CohortCompound(base.Base):
    __tablename__ = 'cohort_compound'
    id = Column(Integer, primary_key=True)
    cohort_id = Column(
        Integer,
        ForeignKey('cohort.id', ondelete='CASCADE'), nullable=False, index=True)
    local_compound_id = Column(String, nullable=False)
    compound_name = Column(Text, nullable=True)
    mz = Column(Numeric(precision=20, scale=12), index=True, nullable=False)
    rt = Column(Numeric(precision=16, scale=10), index=True, nullable=False)
    cross_variation = Column(Numeric(precision=12, scale=6), index=True)
    ml_score = Column(Numeric(precision=9, scale=8), index=True)
    median_measurement = Column(Numeric(precision=80, scale=30), index=True, nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    presence_percentage = Column(Numeric(precision=4, scale=1), nullable=True)
    __table_args__ = (
        UniqueConstraint("cohort_id", "local_compound_id", name="uniq_cohort_id_local_compound_id"),
        Index("ix_cohort_compound_on_cohort_id_mz", "cohort_id", "mz"),
        Index("ix_cohort_compound_on_cohort_id_rt", "cohort_id", "rt"), )

    cohort = relationship("Cohort", backref="metabolites")
    subjects = relationship("Subject", secondary="cohort")

    def __init__(self, cohort, local_compound_id, mz, rt, cross_variation, ml_score, median_measurement=None):
        self.cohort = cohort
        self.local_compound_id = local_compound_id
        self.mz = mz
        self.rt = rt
        self.cross_variation = cross_variation
        self.ml_score = ml_score
        if median_measurement is not None:
            self.median_measurement = median_measurement
