import indices
from datetime import datetime
from elasticsearch import Elasticsearch
from db import db_connection
from models import *
from sqlalchemy.orm import joinedload
import sys
import os
import re
import csv
from helpers import string_to_boolean, is_numeric

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')])
INDEX_NAME = 'metabolomics'
DOC_TYPE = 'metabolite'
DEFAULT_BATCH_SIZE = 10000
MAX_THREAD_COUNT = 4


def find_measurements(metabolite, subject, cohort, session):
    return session.query(Measurement).options(
        joinedload("dataset")
    ).filter(
        Measurement.subject_id == subject.id,
        Measurement.cohort_compound_id == metabolite.id,
    ).all()


def build_metabolite_document(metabolite, subject, cohort, measurements):
    document_id = 'm' + str(metabolite.id) + '_s' + str(subject.id)
    document = {}
    document['COHORT'] = cohort.name
    document['subject'] = subject.local_subject_id
    document['source'] = cohort.source()
    document['MS_method'] = cohort.ms_method()
    document['local_ID'] = metabolite.local_compound_id
    document['MZ'] = metabolite.mz
    document['RT'] = metabolite.rt
    document['ML_score'] = metabolite.ml_score
    document['measurement'] = [
        {'normalization': mmt.dataset.units, 'value': mmt.measurement}
        for mmt
        in measurements
    ]
    document['created'] = datetime.now()
    return [document_id, document]

def find_metabolites(cohort, args, session):
    min_id, max_id = args.metabolite_id_range or [0, 1e20]
    return session.query(CohortCompound).filter(
        CohortCompound.cohort_id == cohort.id,
        CohortCompound.id >= min_id,
        CohortCompound.id <= max_id
    ).order_by(
        CohortCompound.id.asc()
    ).all()

def multithread(cohort, args, session):
    thread_count = 0
    args.auto_batch = False
    batch_size = args.multithread_batch_size or DEFAULT_BATCH_SIZE
    min_id, max_id = [0, batch_size]
    while thread_count < MAX_THREAD_COUNT and session.query(CohortCompound).filter(CohortCompound.cohort_id == cohort.id, CohortCompound.id >= min_id).first() is not None:
        cmd = 'python ' + ' '.join(sys.argv) + ' --metabolite-id-range {} {} > metab_populate_{}.{}.{}.out 2>&1 &'.format(min_id, max_id, args.cohort_name, min_id, max_id)
        print "os.sytem({})".format(cmd)
        os.system(cmd)
        thread_count += 1
        min_id += batch_size
        max_id += batch_size

def run(args):
    if args.action == 'create':
        es.indices.create(index=INDEX_NAME, body=indices.metabolomics.index)
    elif args.action == 'delete':
        es.indices.delete(index=INDEX_NAME)
    elif args.action == 'put_settings':
        print 'Not yet tested'
        pass
    elif args.action == 'put_mapping':
        es.indices.put_mapping(index=INDEX_NAME, doc_type=DOC_TYPE, body=indices.metabolomics.index['mappings'][DOC_TYPE])
    elif args.action == 'populate':
        assert args.cohort_name is not None, "Missing --cohort-name"
        session = db_connection.session_factory()
        cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
        assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
        line_count = 0
        if args.multithread:
            return multithread(cohort, args, session)
        for metabolite in find_metabolites(cohort, args, session):
            for subject in metabolite.subjects:
                line_count += 1
                measurements = find_measurements(metabolite, subject, cohort, session)
                doc_id, document = build_metabolite_document(metabolite, subject, cohort, measurements)
                if args.verbose:
                    print "Indexing {} for (subject, local_ID) ({}, {}). Count is {}".format(doc_id, document['subject'], document['local_ID'], line_count)
                es.index(index=INDEX_NAME, doc_type=DOC_TYPE, id=doc_id, body=document)
