# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Integer, Index, Numeric, UniqueConstraint


def measurement_class_factory(cohort):
    def get_tablename():
        if cohort.name in ["FHS", "FINRISK"]:
            return "fhs_finrisk_measurement"
        elif cohort.name == "MESA":
            return "mesa_measurement"
        elif cohort.name in ["VITAL 400", "VITAL CTSC"]:
            return "vital_measurement"
        else:
            raise Exception('Could not find measurement table for cohort')

    class MeasurementClass(base.Base):
        __tablename__ = get_tablename()
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

        metabolite = relationship('CohortCompound', uselist=False, primaryjoin='foreign(CohortCompound.id) == MeasurementClass.cohort_compound_id')
        dataset = relationship('Dataset', uselist=False, primaryjoin='foreign(Dataset.id) == MeasurementClass.dataset_id')
        sample = relationship('Sample', uselist=False, primaryjoin='foreign(Sample.id) == MeasurementClass.sample_id')

        def __init__(self, sample, dataset, cohort_compound, measurement):
            self.sample_id = sample.id
            self.dataset_id = dataset.id
            self.cohort_compound_id = cohort_compound.id
            self.measurement = measurement

    return MeasurementClass
