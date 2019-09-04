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
INDEX_NAME = 'microbiome_alignments'
DOC_TYPE = 'microbiome_alignment'
CSV_CHUNKSIZE = 3000

FIELDS = { 
    "variant_id": str,
    "qseqid": int,
    "length": int,
    "qstart": int,
    "qend": int,
    "sstart": int,
    "send": int,
    "slen": int,
    "score": int,
    "match": int,
    "mismatch": int,
    "gapopen": int,
    "gapextend": float,
    "pctsim": float,
    "strain": str,
    "copy_number": int,
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
    assert args.cohort_name is not None, "Missing --cohort-name"
    assert args.microbiome_file is not None, "Missing --microbiome-file"
    line_count = 0
    for df in pd.read_csv(args.microbiome_file, chunksize=CSV_CHUNKSIZE, delim_whitespace=True):
        es_inserts = []
        for _, row in df.iterrows():
            line_count += 1
            if not has_all_fields(row):
                continue
            doc = build_document(row)
            doc['study'] = args.cohort_name
            doc['created'] = datetime.now().strftime("%s")
            es_inserts.append({
                "_index": INDEX_NAME,
                "_id": doc['study'] + "_" + doc['strain'] + "_qseqid" + str(doc['qseqid']),
                "_type": DOC_TYPE,
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
