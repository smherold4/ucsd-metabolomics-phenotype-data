# coding=utf-8

import datetime
from db import base
from sqlalchemy.orm import validates
from sqlalchemy import Column, String, Integer, Index


class Cohort(base.Base):
    __tablename__ = 'cohort'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def ms_method(self):
        # This is a shim until I move the method field from dataset to cohort table
        return 'LCMS'

    def source(self):
        # This is a shim until I add the method 'source' to the cohort table
        return 'plasma'
