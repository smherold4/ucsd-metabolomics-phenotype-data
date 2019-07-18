# coding=utf-8

import datetime
from db import base
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
