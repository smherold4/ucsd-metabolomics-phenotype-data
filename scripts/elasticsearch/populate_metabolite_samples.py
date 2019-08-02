import indices
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from db import db_connection
from models import *
from sqlalchemy.orm import joinedload
import sys
import os
import re
import csv

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')])
INDEX_NAME = 'metabolite_samples'
DOC_TYPE = 'metabolite_sample'
DEFAULT_BATCH_SIZE = 40000


def run(args):
    assert args.cohort_name is not None, "Missing --cohort-name"
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    line_count = 0

    last_queried_id = 0
    while last_queried_id is not None:
      sql = session.query(Measurement).filter(
          Measurement.dataset_id == Dataset.id,
          Sample.cohort_id == cohort.id,
          Measurement.cohort_compound_id == CohortCompound.id,
          Measurement.id > last_queried_id,
      ).join(
          Measurement.sample,
      ).join(
          Subject, Sample.subject_id == Subject.id, isouter=True,
      ).with_entities(
          Measurement.id,
          Measurement.measurement,
          Dataset.units,
          CohortCompound.local_compound_id,
          CohortCompound.ml_score,
          CohortCompound.mz,
          CohortCompound.rt,
          Sample.sample_barcode,
          Sample.plate_well,
          Subject.local_subject_id,
      ).order_by(
          Measurement.id.asc()
      ).limit(args.index_batch_size or DEFAULT_BATCH_SIZE)
      mmts = sql.all()
      last_queried_id = mmts[-1].id if len(mmts) else None
      es_inserts = [
        {
          "_index": INDEX_NAME,
          "_type": DOC_TYPE,
          "_id": cohort.name + "_" + str(mmt.id), # careful when changing this
          "_source": {
              "cohort": cohort.name,
              "created": datetime.now(),
              "local_ID": mmt.local_compound_id,
              "measurement_{}".format(mmt.units): mmt.measurement,
              "method": cohort.method,
              "ML_score": mmt.ml_score,
              "MZ": mmt.mz,
              "plate_well": mmt.plate_well,
              "RT": mmt.rt,
              "sample_barcode": mmt.sample_barcode,
              "subject": mmt.local_subject_id,
          }
        }
        for mmt in mmts
      ]
      if args.verbose:
          print "Inserting {} {} documents for {}.  On ".format(len(mmts), args.index, cohort.name)
      helpers.bulk(es, es_inserts)
