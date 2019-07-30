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
import numpy
from helpers.data_types import determine_dtype_of_df_column
from collections import defaultdict

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')])
INDEX_NAME = 'subjects'
DOC_TYPE = 'subject'
CSV_CHUNKSIZE = 2000

class CompoundMeasurementGroup:

  def __init__(self):
      self.measurements = []
      self.local_compound_id = None
      self.MZ = None
      self.RT = None

  def add(self, mmt):
      self.measurements.append(mmt)
      self.local_compound_id = mmt.local_compound_id
      self.MZ = mmt.mz
      self.RT = mmt.rt


def feature_json(group):
    return {
        "local_ID": group.local_compound_id,
        "MZ": group.MZ,
        "RT": group.RT,
        "measurements": [{"value": mmt.measurement, "normalization": mmt.units} for mmt in group.measurements]
    }


def measurements_by_compound(sample, session):
    # We could use a SQL group by here
    sql = session.query(
        Measurement
    ).filter(
        Measurement.sample_id == sample.id,
        Measurement.cohort_compound_id == CohortCompound.id,
        Measurement.dataset_id == Dataset.id,
    ).with_entities(
        Measurement.measurement,
        CohortCompound.local_compound_id,
        CohortCompound.mz,
        CohortCompound.rt,
        Dataset.units,
    )
    result = defaultdict(CompoundMeasurementGroup)
    for mmt in sql.all():
        result[mmt.local_compound_id].add(mmt)
    return result


def sample_json(session, sample, cohort, age_at_sample_collection):
    result = {
        "source": cohort.source(),
        "sample_barcode": sample.sample_barcode,
        "metabolite_dataset": [
            {
                "plate_well": sample.plate_well,
                "method": cohort.method,
                "features": [
                    feature_json(compound_measurement_group)
                    for _, compound_measurement_group
                    in measurements_by_compound(sample, session).iteritems()
                ]
            }
        ]
    }
    if age_at_sample_collection:
        result["age_at_sample_collection"] = age_at_sample_collection
        result["sample_phenotypes"] = [{
            "name": "age_at_sample_collection",
            "float": age_at_sample_collection,
        }]
    return result


def determine_data_types_by_column(df):
    result = {}
    for col in df.columns:
        dtype, dseries = determine_dtype_of_df_column(df, col)
        result[col] = {
            'type': dtype,
            'series': dseries
        }
    return result


def build_subject_document(subject, age_at_sample_collection, phenotype_data, cohort, session):
    data = {}
    data['subject'] = subject.local_subject_id
    data['cohort'] = cohort.name
    data['samples'] = [
        sample_json(session, sample, cohort, age_at_sample_collection)
        for sample
        in subject.samples
    ]
    data['phenotypes'] = [{'name': key, val['type']: val['value']} for key, val in phenotype_data.iteritems() if key]
    data['created'] = datetime.now()
    return [subject.id, data]


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
        assert args.age_at_sample_collection_label is not None, "Must specify --age-at-sample-collection-label"
        assert args.subject_id_label is not None, "Must specify --subject-id-label"
        line_count = 0
        for df in pd.read_csv(args.file, chunksize=CSV_CHUNKSIZE):
            data_typed_by_col = determine_data_types_by_column(df)
            for _, row in df.iterrows():
                line_count += 1
                row_data = row_with_proper_types(data_typed_by_col, row.name)
                subject_id = row[args.subject_id_label]
                age_at_sample_collection = row[args.age_at_sample_collection_label]
                if pd.isnull(subject_id):
                    continue
                subject = session.query(Subject).filter(
                    Subject.cohort_id == cohort.id,
                    Subject.local_subject_id == subject_id
                ).first()
                if subject is None:
                    continue
                doc_id, document = build_subject_document(
                    subject,
                    age_at_sample_collection,
                    row_data,
                    cohort,
                    session)
                if document:
                    if args.verbose:
                        print "Indexing doc {} for subject_id: {}. Count is {}".format(doc_id, subject.local_subject_id, line_count)
                    es.index(index=INDEX_NAME, doc_type=DOC_TYPE, id=doc_id, body=document)
