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
INDEX_NAME = 'microbiome_abundances'
DOC_TYPE = 'microbiome_abundance'
CSV_CHUNKSIZE = 3000

FIELDS = {
    "dataset": str,
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
    for df in pd.read_csv(args.microbiome_file, chunksize=CSV_CHUNKSIZE, delim_whitespace=True):
        es_inserts = []
        for _, row in df.iterrows():
            line_count += 1
            if not has_all_fields(row):
                continue
            doc = build_document(row)

            for species in row['species'].split(","):
                if pd.isnull(species):
                    continue
                doc['species'] = species
                es_inserts.append({
                    "_index": INDEX_NAME,
                    "_type": DOC_TYPE,
                    "_id": doc['dataset'] + "_" + doc['sample_id'] + "_" + doc['species'],
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
