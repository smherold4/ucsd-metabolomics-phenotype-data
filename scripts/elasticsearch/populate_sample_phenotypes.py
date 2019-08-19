import indices
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from db import db_connection
from models import *
import sys
import os
import re
import csv
import pandas as pd
import numpy
from helpers.data_types import determine_dtype_of_df_column
from collections import defaultdict

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')], timeout=30)
INDEX_NAME = 'sample_phenotypes'
DOC_TYPE = 'sample_phenotype'
CSV_CHUNKSIZE = 3000

def determine_data_types_by_column(df):
    result = {}
    for col in df.columns:
        dtype, dseries = determine_dtype_of_df_column(df, col)
        result[col] = {
            'type': dtype,
            'series': dseries
        }
    return result


def row_with_proper_types(data_typed_by_col, row_idx):
    result = {}
    for col in data_typed_by_col:
        if row_idx not in data_typed_by_col[col]['series']:
            continue
        value = data_typed_by_col[col]['series'][row_idx]
        # numpy booleans can't be serialized
        if isinstance(value, numpy.bool_):
            value = not not value
        result[col] = {'type': data_typed_by_col[col]['type'], 'value': value}
    return result


def run(args):
  assert args.cohort_name is not None, "Missing --cohort-name"
  session = db_connection.session_factory()
  cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
  assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
  assert args.phenotype_file is not None, "Must specify --phenotype-file path for phenotype data"
  assert args.subject_id_label is not None, "Must specify --subject-id-label"
  line_count = 0
  for df in pd.read_csv(args.phenotype_file, chunksize=CSV_CHUNKSIZE):
      data_typed_by_col = determine_data_types_by_column(df)
      for _, row in df.iterrows():
          line_count += 1
          row_data = row_with_proper_types(data_typed_by_col, row.name)
          local_subject_id = row[args.subject_id_label]
          if pd.isnull(local_subject_id):
              continue
          subject = session.query(Subject).filter(
              Subject.cohort_id == cohort.id,
              Subject.local_subject_id == str(local_subject_id),
          ).first() or Subject(cohort, str(local_subject_id))
          if not subject.id:
              session.add(subject):
              session.commit()
          assert args.exam_no is not None, "Currently requiring --exam-no"
          cohort_sample_id = str(local_subject_id) + "-" + args.exam_no
          sample = session.query(Sample).filter(
              Sample.cohort_sample_id == cohort_sample_id,
              Sample.subject_id == subject.id,
          ).first() or Sample(cohort.id, subject.id, cohort_sample_id, None, None)
          if not sample.id:
              session.add(sample)
              session.commit()
          sample_barcode_or_backup = sample.sample_barcode or cohort_sample_id
          es_inserts = [
              {
                  "_index": INDEX_NAME,
                  "_type": DOC_TYPE,
                  "_id": cohort.name + "_" + phenotype_name.replace(" ", "_") + "_" + sample_barcode_or_backup, # careful when changing this
                  "_source": {
                      "study": cohort.name,
                      "subject": subject.local_subject_id,
                      "sample_barcode": sample_barcode_or_backup,
                      "name": phenotype_name,
                      phenotype_value_data['type']: phenotype_value_data['value'],
                  }
              }
              for phenotype_name, phenotype_value_data in row_data.iteritems()
          ]
          if args.verbose:
              print "Inserting {} {} documents for {}.  Line count is {}".format(
                  len(es_inserts),
                  args.index,
                  subject.local_subject_id,
                  line_count,
              )
          for success, info in helpers.parallel_bulk(es, es_inserts):
              if not success:
                  print('Parallel bulk failure:', info)
                  raise Exception(info)
