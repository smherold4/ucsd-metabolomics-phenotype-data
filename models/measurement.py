# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Index, Numeric, UniqueConstraint


class Measurement(base.Base):
    __tablename__ = 'measurement'
    id = Column(Integer, primary_key=True)
    sample_id = Column(
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

    metabolite = relationship('CohortCompound', uselist=False, primaryjoin='foreign(CohortCompound.id) == Measurement.cohort_compound_id')
    dataset = relationship('Dataset', uselist=False, primaryjoin='foreign(Dataset.id) == Measurement.dataset_id')
    sample = relationship('Sample', uselist=False, primaryjoin='foreign(Sample.id) == Measurement.sample_id')

    def __init__(self, sample, dataset, cohort_compound, measurement):
        self.sample_id = sample.id
        self.dataset_id = dataset.id
        self.cohort_compound_id = cohort_compound.id
        self.measurement = measurement

    @classmethod
    def configure_tablename(cls, cohort):
        if cohort.name in ["FHS", "FINRISK"]:
            cls.__tablename__ = "fhs_finrisk_measurement"
        elif cohort.name == "MESA":
            cls.__tablename__ = "mesa_measurement"
        else:
            raise Exception('Could not find measurement table for cohort')
