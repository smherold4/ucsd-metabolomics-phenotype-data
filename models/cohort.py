# coding=utf-8

import datetime
from db import base
from sqlalchemy import Column, String, Integer, Index


class Cohort(base.Base):
    __tablename__ = 'cohort'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    source = Column(String)

    def phenotypes_data_index(self):
        if self.name in ['MESA']:
            return 'sample_phenotypes'
        else:
            return 'subject_phenotypes'
