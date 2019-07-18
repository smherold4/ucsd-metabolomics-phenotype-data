# coding=utf-8

import datetime
from models import CohortCompound
from db import base, db_connection
from sqlalchemy.orm import validates
from sqlalchemy import Column, String, Date, Integer, Numeric, Index, DateTime
  
class Compound(base.Base):
  __tablename__ = 'compound'
  id = Column(Integer, primary_key=True)
  pub_chem_cid = Column(Integer, index=True)
  mz = Column(Numeric(precision=20, scale=12), index=True, nullable=False)
  rt = Column(Numeric(precision=16, scale=10), index=True, nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, mz, rt):
    self.mz = mz
    self.rt = rt

  @classmethod
  def merge(compound_to_keep, compound_to_remove):
    assert type(compound_to_keep) == Compound, "compound_to_keep must be an instance of a Compound"
    assert type(compound_to_remove) == Compound, "compound_to_remove must be an instance of a Compound"
    # migrate cohort_compounds, delete  compound_to_remove
    session = db_connection.session_factory()
    session.query(CohortCompound) \
      .filter(CohortCompound.compound_id==compound_to_remove.id) \
      .update({'compound_id': compound_to_keep.id})
