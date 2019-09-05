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
INDEX_NAME = 'microbiome_abundances'
DOC_TYPE = 'microbiome_abundance'
CSV_CHUNKSIZE = 3000

FIELDS = {
    "sample_id": str,
    "osu_id": str,
    "osu_count": int,
    "pctsim": float,
    "species": str,
}

def has_all_fields(row):
    for field in FIELDS.keys():
        if pd.isnull(row[field]):
            return False
    return True

def build_document(row):
    result = {}
    for field, dtype in FIELDS.iteritems():
        result[field] = dtype(row[field])
    return result


def run(args):
    line_count = 0
    assert args.cohort_name is not None, "Missing --cohort-name"
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    assert args.microbiome_file is not None, "Missing --microbiome-file"
    for df in pd.read_csv(args.microbiome_file, chunksize=CSV_CHUNKSIZE, delim_whitespace=True):
        es_inserts = []
        for _, row in df.iterrows():
            line_count += 1
            if not has_all_fields(row):
                continue
            doc = build_document(row)
            doc['study'] = cohort.name
            doc['subjectID'] = doc.pop('sample_id')
            doc['created'] = datetime.now().strftime("%s")
            doc['species'] = doc['species'].replace('_', ' ')
            es_inserts.append({
                "_index": INDEX_NAME,
                "_type": DOC_TYPE,
                "_id": cohort.name.replace(" ", "_") + "_" + doc['subjectID'] + "_" + doc['osu_id'],
                "_source": doc
            })
        if args.verbose:
            print "Inserting {} {} documents.  Line count is {}".format(
                len(es_inserts),
                args.index,
                line_count,
            )
        for success, info in helpers.parallel_bulk(es, es_inserts):
            if not success:
                print('Parallel bulk failure:', info)
                raise Exception(info)
