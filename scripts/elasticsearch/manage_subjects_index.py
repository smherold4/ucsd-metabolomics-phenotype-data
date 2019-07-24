import indices
from datetime import datetime
from elasticsearch import Elasticsearch
from db import db_connection
from models import *
import sys
import os
import re
import csv
import pandas as pd
from helpers import string_to_boolean

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')])
INDEX_NAME = 'subjects'
DOC_TYPE = 'subject'
BATCH_SIZE = 2000
CSV_CHUNKSIZE = 1


def measurement_json(measurement):
    return {
        "local_ID": measurement.local_compound_id,
        "value": measurement.measurement,
    }


def find_measurements(dataset, subject, session):
    sql = session.query(
        Measurement
    ).filter(
        Measurement.dataset_id == dataset.id,
        Measurement.subject_id == subject.id,
        Measurement.cohort_compound_id == CohortCompound.id,
    ).with_entities(Measurement.measurement, CohortCompound.local_compound_id)
    return sql.all()


def metabolite_dataset(subject, cohort, session):
    result = []
    for dataset in subject.datasets:
        measurements = find_measurements(dataset, subject, session)
        result.append({
            "source": cohort.source(),
            "method": cohort.ms_method(),
            "normalization": dataset.units,
            "measurements": [measurement_json(mmt) for mmt in measurements]})
    return result


def build_subject_document(pandas_series, cohort, session, args):
    csv_data = pandas_series.dropna().to_dict()
    subject_id = csv_data.get(args.subject_id_label)
    if pd.isnull(subject_id):
        return [None, None, None]
    subject = session.query(Subject).filter(
        Subject.local_subject_id == subject_id,
        Subject.cohort_id == cohort.id
    ).first()
    if subject is None:
        if args.verbose:
            print "Could not find subject: local_subject_id: {}, cohort_id: {}".format(subject_id, cohort.id)
        return [None, None, None]

    data = {}
    data['SUBJECT'] = subject_id
    data['COHORT'] = subject.cohort.name
    data['phenotypes'] = [{'name': key, 'value': val } for key, val in csv_data.iteritems() if key and type(val) in [int, float]]
    data['metabolite_dataset'] = metabolite_dataset(subject, cohort, session)
    data['created'] = datetime.now()
    return [subject.id, subject_id, data]


def run(args):
    if args.action == 'create':
        es.indices.create(index=INDEX_NAME, body=indices.subjects.index)
    elif args.action == 'delete':
        es.indices.delete(index=INDEX_NAME)
    elif args.action == 'put_settings':
        print 'Not yet tested'
        pass
        # es.indices.close(index=INDEX_NAME)
        # es.indices.put_settings(index=INDEX_NAME, body='????')
        # es.indices.open(index=INDEX_NAME)
    elif args.action == 'put_mapping':
        es.indices.put_mapping(index=INDEX_NAME, doc_type=DOC_TYPE, body=indices.subjects.index['mappings'][DOC_TYPE])
    elif args.action == 'populate':
        assert args.cohort_name is not None, "Missing --cohort-name"
        session = db_connection.session_factory()
        cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
        assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
        assert args.file is not None, "Must specify --file path for phenotype data"
        line_count = 0
        for df in pd.read_csv(args.file, chunksize=CSV_CHUNKSIZE):
            for _, row in df.iterrows():
                line_count += 1
                doc_id, subject_id, document = build_subject_document(row, cohort, session, args)
                if document:
                    if args.verbose:
                        print "Indexing doc {} for subject: {}. Count is {}".format(doc_id, subject_id, line_count)
                    es.index(index=INDEX_NAME, doc_type=DOC_TYPE, id=doc_id, body=document)
