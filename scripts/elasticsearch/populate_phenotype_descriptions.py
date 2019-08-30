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
import pandas as pd
from pandasticsearch import Select

COLUMNS = {
    'variable_name': 0,
    'description': 1
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
            description = row[COLUMNS['description']] and unicode(row[COLUMNS['description']], 'UTF-8')
            if pd.isnull(variable_name):
                continue
            doc_id = "{}_{}".format(cohort.name, variable_name)  # careful when changing this
            datatype = get_datatype_for_phenotype(variable_name, cohort)
            es.index(index=INDEX_NAME, doc_type=DOC_TYPE, id=doc_id, body={
                "datatype": datatype,
                "description": description,
                "study": cohort.name,
                "variable_name": variable_name,
            })
            if args.verbose:
                print "Indexed {}".format(variable_name)


def get_datatype_for_phenotype(variable_name, cohort):
    query = {
        "bool": {
            "must": [
                {
                    "term": {
                        "study": cohort.name
                    }
                },
                {
                    "term": {
                        "name": variable_name
                    }
                },
            ]
        }
    }
    res = es.search(index=cohort.phenotypes_data_index(), body={"query": query}, size=10)
    df = Select.from_dict(res).to_pandas()
    if df is None:
        return None
    for datatype in ['float', 'boolean', 'integer', 'string']:
        if datatype in df:
            return datatype
