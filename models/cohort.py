# coding=utf-8

import datetime
from db import base
from sqlalchemy import Column, String, Integer, Index


class Cohort(base.Base):
    __tablename__ = 'cohort'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    method = Column(String, nullable=False)
    cohort_sample_id_label = Column(String)

    def __init__(self, name, method):
        self.name = name
        self.method = method

    def source(self):
        # This is a shim until I add the method 'source' to the cohort table
        return 'plasma'
