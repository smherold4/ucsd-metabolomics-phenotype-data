# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Index, Numeric, ForeignKey, UniqueConstraint


class Sample(base.Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    subject_id = Column(
        Integer,
        ForeignKey(
            'subject.id',
            ondelete='CASCADE'),
        nullable=False,
        index=True)
    cohort_compound_id = Column(
        Integer,
        ForeignKey(
            'cohort_compound.id',
            ondelete='CASCADE'),
        nullable=False,
        index=True)
    measurement = Column(Numeric(precision=80, scale=30), nullable=False)
    median_absolute_deviation = Column(
        Numeric(precision=7, scale=4), nullable=True)
    __table_args__ = (
        UniqueConstraint(
            "subject_id",
            "cohort_compound_id",
            name="uniq_sample"),
        Index(
            "ix_sample_on_cohort_compound_measurement",
            "cohort_compound_id",
            "measurement"),
        Index(
            "ix_sample_on_cohort_compound_mad",
            "cohort_compound_id",
            "median_absolute_deviation"),
    )

    subject = relationship("Subject")
    cohort_compound = relationship("CohortCompound")

    def __init__(self, subject, cohort_compound, measurement):
        self.subject = subject
        self.cohort_compound = cohort_compound
        self.measurement = measurement
