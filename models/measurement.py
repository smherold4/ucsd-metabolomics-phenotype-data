# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Index, Numeric, ForeignKey, UniqueConstraint


class Measurement(base.Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    subject_id = Column(
        Integer,
        ForeignKey('subject.id', ondelete='CASCADE'),
        nullable=False,
        index=True)
    cohort_compound_id = Column(
        Integer,
        ForeignKey('cohort_compound.id', ondelete='CASCADE'),
        nullable=False)
    dataset_id = Column(
        Integer,
        ForeignKey('dataset.id', ondelete='CASCADE'),
        nullable=False)
    measurement = Column(
        Numeric(precision=80, scale=30),
        nullable=False)
    median_absolute_deviation = Column(
        Numeric(precision=7, scale=4), nullable=True)
    __table_args__ = (
        UniqueConstraint(
            "subject_id",
            "cohort_compound_id",
            "dataset_id",
            name="uniq_measurement"),
        Index(
            "ix_measurement_on_cohort_compound_measurement",
            "cohort_compound_id",
            "measurement"),
        Index(
            "ix_measurement_on_dataset_measurement",
            "dataset_id",
            "measurement"),
        Index(
            "ix_measurement_on_cohort_compound_mad",
            "cohort_compound_id",
            "median_absolute_deviation"),
        Index(
            "ix_measurement_on_dataset_compound",
            "dataset_id",
            "cohort_compound_id"),
    )

    subject = relationship("Subject")
    cohort_compound = relationship("CohortCompound")
    dataset = relationship("Dataset")

    def __init__(self, subject, cohort_compound, measurement):
        self.subject = subject
        self.cohort_compound = cohort_compound
        self.measurement = measurement
