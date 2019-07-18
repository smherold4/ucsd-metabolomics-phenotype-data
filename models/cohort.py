# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Date, Integer, Numeric, Index, DateTime, ForeignKey, UniqueConstraint
  
class Cohort(base.Base):
  __tablename__ = 'cohort'
  id = Column(Integer, primary_key=True)
  study_id = Column(Integer, ForeignKey('study.id'))
  method = Column(String, nullable=False, index=True)
  units = Column(String, nullable=False, index=True)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  __table_args__ = (UniqueConstraint("study_id",  "method", "units", name="uniq_study_method_units"),)

  METHODS = ['LCMS', 'Eicosanoid']
  UNITS = ['raw', 'normalized']

  study = relationship("Study")

  @validates('method')
  def validate_method(self, key, value):
    assert value in Cohort.METHODS
    return value

  @validates('units')
  def validate_units(self, key, value):
    assert value in Cohort.UNITS
    return value

  def __init__(self, study, method, units):
    self.study_id = study.id
    self.method = method
    self.units = units
