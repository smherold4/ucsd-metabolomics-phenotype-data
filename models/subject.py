# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Index, DateTime, ForeignKey, UniqueConstraint


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
    created = Column(DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        UniqueConstraint(
            "cohort_id",
            "local_subject_id",
            name="uniq_cohort_subject"),
    )

    cohort = relationship("Cohort")

    def __init__(self, cohort, local_subject_id):
        self.local_subject_id = local_subject_id
        self.cohort = cohort
