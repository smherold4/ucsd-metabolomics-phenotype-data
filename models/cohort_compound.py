# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Date, Integer, Numeric, Index, DateTime, ForeignKey, UniqueConstraint
  
class CohortCompound(base.Base):
  __tablename__ = 'cohort_compound'
  id = Column(Integer, primary_key=True)
  cohort_id = Column(Integer, ForeignKey('cohort.id', ondelete='CASCADE'), nullable=False)
  compound_id = Column(Integer, ForeignKey('compound.id'), nullable=False)
  local_compound_id = Column(String, nullable=False, index=True)
  cross_variation = Column(Numeric(precision=12, scale=6), index=True)
  ml_score = Column(Numeric(precision=9, scale=8), index=True)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  __table_args__ = (
    UniqueConstraint("cohort_id",  "local_compound_id", name="uniq_cohort_id_local_compound_id"),
  )

  cohort = relationship("Cohort")
  compound = relationship("Compound")

  def __init__(self, cohort, compound, local_compound_id, cross_variation, ml_score):
    self.cohort = cohort
    self.compound = compound
    self.local_compound_id = local_compound_id
    self.cross_variation = cross_variation
    self.ml_score = ml_score
  