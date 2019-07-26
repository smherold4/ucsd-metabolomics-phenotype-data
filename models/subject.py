# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Numeric, Index, DateTime, ForeignKey, UniqueConstraint


class Subject(base.Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    local_subject_id = Column(String, nullable=False, index=True)
    cohort_id = Column(
        Integer,
        ForeignKey(
            'cohort.id',
            ondelete='CASCADE'),
        nullable=False)
    sample_barcode = Column(String)
    plate_well = Column(String)
    age_at_sample_collection = Column(Numeric(precision=8, scale=4))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        UniqueConstraint(
            "cohort_id",
            "local_subject_id",
            name="uniq_cohort_subject"),
    )

    cohort = relationship("Cohort", backref="subjects")
    datasets = relationship("Dataset", secondary="cohort")

    def __init__(self, cohort, local_subject_id):
        self.local_subject_id = local_subject_id
        self.cohort = cohort
