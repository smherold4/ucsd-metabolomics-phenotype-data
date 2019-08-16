import indices
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from db import db_connection
from models import *
from sqlalchemy.orm import joinedload
import sys
import os
import re
import csv

COLUMNS = {
  'variable_name': 0,
  'description':   1
}

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')], timeout=30)
INDEX_NAME = 'phenotype_descriptions'
DOC_TYPE = 'phenotype_description'
DEFAULT_BATCH_SIZE = 40000

def run(args):
    assert args.cohort_name is not None, "Missing --cohort-name"
    assert args.phenotype_file is not None, "Missing --phenotype-file"
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)

    with open(args.phenotype_file) as csvfile:
        line_count = 0
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            line_count += 1
            if line_count == 1:
              continue
            variable_name = row[COLUMNS['variable_name']]
            description = row[COLUMNS['description']]
            es
            import pdb; pdb.set_trace()
            es.index(index="test-index", doc_type='tweet', id=1, body=doc)
            # get the datatype for this phenotype
            # insert the doc
