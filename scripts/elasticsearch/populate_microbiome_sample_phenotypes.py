import indices
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
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
INDEX_NAME = 'microbiome_sample_phenotypes'
DOC_TYPE = 'microbiome_sample_phenotype'
CSV_CHUNKSIZE = 3000

REQUIRED_FIELDS = {
    "subject": str,
    "sample_id": str,
    "variable": str,
    "value": str,
}

ADDITIONAL_FIELDS = {}

def all_fields():
    result = REQUIRED_FIELDS.copy()
    result.update(ADDITIONAL_FIELDS)
    return result

def has_required_fields(row):
    for field in REQUIRED_FIELDS.keys():
        if pd.isnull(row[field]):
            return False
    return True


def build_document(row):
    result = {}
    for field, dtype in all_fields().iteritems():
        result[field] = dtype(row[field])
    return result


def run(args):
    line_count = 0
    assert args.cohort_name is not None, "Missing --cohort-name"
    assert args.microbiome_file is not None, "Missing --microbiome-file"
    for df in pd.read_csv(args.microbiome_file, chunksize=CSV_CHUNKSIZE, sep=','):
        es_inserts = []
        for _, row in df.iterrows():
            line_count += 1
            if not has_required_fields(row):
                continue
            doc = build_document(row)
            doc['study'] = args.cohort_name
            doc['created'] = datetime.now().strftime("%s")
            es_inserts.append({
                "_index": INDEX_NAME,
                "_type": DOC_TYPE,
                "_id": args.cohort_name.replace(" ", "_") + "_" + doc['subject'] + "_" + doc['sample'] + "_" + doc['variable'],
                "_source": doc
            })
        print "Inserting {} {} documents.  Line count is {}".format(
            len(es_inserts),
            args.index,
            line_count,
        )
        for success, info in helpers.parallel_bulk(es, es_inserts):
            if not success:
                print('Parallel bulk failure:', info)
                raise Exception(info)
