# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates
from sqlalchemy import Column, String, Integer, Index
  
class Study(base.Base):
  __tablename__ = 'study'
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False, unique=True)
  
  def __init__(self, name):
    self.name = name
