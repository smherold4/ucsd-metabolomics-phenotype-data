# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Numeric, Index, DateTime, ForeignKey, UniqueConstraint, CheckConstraint


class Sample(base.Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    subject_id = Column(
        Integer,
        ForeignKey('subject.id', ondelete='CASCADE'),
        nullable=True)
    cohort_id = Column(
        Integer,
        ForeignKey('cohort.id', ondelete='CASCADE'),
        nullable=False)
    cohort_sample_id = Column(String)
    sample_barcode = Column(String)
    plate_well = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        UniqueConstraint(
            "subject_id",
            "cohort_sample_id",
            name="ix_sample_uniq_subject_cohort_sample_id"),
        UniqueConstraint(
            "cohort_id",
            "cohort_sample_id",
            name="ix_sample_uniq_cohort_cohort_sample_id"),
        CheckConstraint('(cohort_sample_id is not null or plate_well is not null)', name='constraint_sample_identifier')
    )

    cohort = relationship("Cohort", backref="samples")
    subject = relationship("Subject", backref="samples")

    def __init__(self, cohort_id, subject_id, cohort_sample_id, sample_barcode, plate_well):
        self.cohort_id = cohort_id
        self.subject_id = subject_id
        self.cohort_sample_id = cohort_sample_id
        self.sample_barcode = sample_barcode
        self.plate_well = plate_well
