import indices
from datetime import datetime
from elasticsearch import Elasticsearch
from db import db_connection
from models import Subject, Cohort
import sys, re, csv
from helpers import string_to_boolean, is_numeric

es = Elasticsearch()
INDEX_NAME = 'subjects'
DOC_TYPE = 'subject'
BATCH_SIZE = 2000
PLASMA_ID_REGEX = r'\d{5}-\d'

COLS = {
  "PLASMA_ID": 0,
  "BL_AGE": 8,
  "BMI": 18,
  "CURR_SMOKE": 22
}

def parse_csv_row(row):
    plasma_id = row[COLS['PLASMA_ID']] if re.search(PLASMA_ID_REGEX, row[COLS['PLASMA_ID']]) else None
    bl_age = row[COLS['BL_AGE']] if is_numeric(row[COLS['BL_AGE']]) else None
    bmi = row[COLS['BMI']] if is_numeric(row[COLS['BMI']]) else None
    curr_smoke = string_to_boolean(row[COLS['CURR_SMOKE']]) if is_numeric(row[COLS['CURR_SMOKE']]) else None
    return [plasma_id, bl_age, bmi, curr_smoke]

def build_subject_document(row, cohort, session, args):
    plasma_id, bl_age, bmi, curr_smoke = parse_csv_row(row)
    if plasma_id is None:
      return [None, None, None]

    subject = session.query(Subject).filter(
        Subject.local_subject_id == plasma_id,
        Subject.cohort_id == cohort.id
    ).first()
    if subject is None:
        if args.verbose:
            print "Could not find subject: local_subject_id: {}, cohort_id: {}".format(plasma_id, cohort.id)
        return [None, None, None]

    document = {
      "PLASMA_ID": plasma_id,
      "BL_AGE": bl_age,
      "BMI": bmi,
      "CURR_SMOKE": curr_smoke,
      "metabolite_dataset": []
    }
    return [subject.id, plasma_id, document]

def run(args):
    if args.action == 'create':
        es.indices.create(index=INDEX_NAME, body=indices.subjects.index)
    elif args.action == 'delete':
        es.indices.delete(index=INDEX_NAME)
    elif args.action == 'populate':
        assert args.cohort_name is not None, "Missing --cohort-name"
        session = db_connection.session_factory()
        cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
        assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
        assert args.file is not None, "Must specify --file path for phenotype data"
        with open(args.file) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            for line_count, row in enumerate(csv_reader):
                if line_count == 0:
                    continue
                doc_id, plasma_id, document = build_subject_document(row, cohort, session, args)
                if document:
                    if args.verbose:
                        print "Indexing line {} for plasma_id: {}".format(line_count, plasma_id)
                    es.index(index=INDEX_NAME, doc_type=DOC_TYPE, id=doc_id, body=document)

    # UPDATE DOC_TYPE MAPPINGS
    # es.indices.put_mapping(index=INDEX_NAME, doc_type='dog', body=dogs.index['mappings']['dog'])

    # UPDATE SETTINGS (must close and open index to add analyzers)
    # es.indices.close(index=INDEX_NAME)
    # es.indices.put_settings(index=INDEX_NAME, body=dogs.index['settings'])
    # es.indices.open(index=INDEX_NAME)

    # INSERT/UPDATE DOCS
    # es.index(index=INDEX_NAME, doc_type='dog', id=1, body=dog.buddy)
    # es.index(index=INDEX_NAME, doc_type='dog', id=2, body=dog.tuffy)
    # es.index(index=INDEX_NAME, doc_type='dog', id=3, body=dog.minnie)

    # DELETE DOCS
    # es.delete(index=INDEX_NAME, doc_type='dog', id=1)
    # es.delete(index=INDEX_NAME, doc_type='dog', id=2)

    # UPDATE DOCS
    # es.update(
    #   index=INDEX_NAME,
    #   doc_type='dog',
    #   id='W_uSzmsBUhRInbGHV2mc',
    #   body={'doc': dog.buddy})
