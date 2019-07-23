# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Index, Numeric, UniqueConstraint


class Measurement(base.Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    subject_id = Column(
        Integer,
        nullable=False)
    cohort_compound_id = Column(
        Integer,
        nullable=False)
    dataset_id = Column(
        Integer,
        nullable=False)
    measurement = Column(
        Numeric(precision=80, scale=30),
        nullable=False)
    median_absolute_deviation = Column(
        Numeric(precision=7, scale=4), nullable=True)
    # __table_args__ = (
    #     UniqueConstraint(
    #         "subject_id",
    #         "cohort_compound_id",
    #         "dataset_id",
    #         name="uniq_measurement"),
    #     Index(
    #         "ix_measurement_on_cohort_compound_measurement",
    #         "cohort_compound_id",
    #         "measurement"),
    #     Index(
    #         "ix_measurement_on_dataset_compound",
    #         "dataset_id",
    #         "cohort_compound_id"),
    # )

    metabolite = relationship('CohortCompound', uselist=False, primaryjoin='foreign(CohortCompound.id) == Measurement.cohort_compound_id')
    dataset = relationship('Dataset', uselist=False, primaryjoin='foreign(Dataset.id) == Measurement.dataset_id')
    subject = relationship('Subject', uselist=False, primaryjoin='foreign(Subject.id) == Measurement.subject_id')

    def __init__(self, subject, cohort_compound, measurement):
        self.subject_id = subject.id
        self.cohort_compound_id = cohort_compound.id
        self.measurement_id = measurement.id
