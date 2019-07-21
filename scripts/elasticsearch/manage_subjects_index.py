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

COLS = {
  "PLASMA_ID": { 'col': 0, 'type': 'numeric' },
  "BL_AGE": { 'col': 8, 'type': 'numeric' },
  "BMI": { 'col': 18, 'type': 'numeric' },
  "CURR_SMOKE": { 'col': 22, 'type': 'boolean' },
  "SODIUM": { 'col': 42, 'type': 'numeric' },
  "KY100_30": { 'col': 118, 'type': 'numeric' },
}

def map_csv_values(row):
    result = {}
    for field, meta in COLS.items():
        val = row[meta['col']]
        dtype = meta['type']
        if dtype == 'numeric':
            result[field] = val if is_numeric(val) else None
        elif dtype == 'boolean':
            result[field] = string_to_boolean(val)
        else:
            result[field] = val
    return result

def build_subject_document(row, cohort, session, args):
    data = map_csv_values(row)
    plasma_id = data['PLASMA_ID']
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

    data['metabolite_dataset'] = []
    data['created'] = datetime.now()
    return [subject.id, plasma_id, data]

def run(args):
    if args.action == 'create':
        es.indices.create(index=INDEX_NAME, body=indices.subjects.index)
    elif args.action == 'delete':
        es.indices.delete(index=INDEX_NAME)
    elif args.action == 'put_settings':
        es.indices.close(index=INDEX_NAME)
        es.indices.put_settings(index=INDEX_NAME, body=indices.subjects.index)
        es.indices.open(index=INDEX_NAME)
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
