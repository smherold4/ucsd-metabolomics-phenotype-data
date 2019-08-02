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

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')])
INDEX_NAME = 'metabolite_alignments'
DOC_TYPE = 'metabolite_alignment'
DEFAULT_BATCH_SIZE = 40000


def build_alignment_dict(args):
    this_cohort_col, alignment_cohort_col = (None, None)
    if args.alignment_cohort_col == 'A':
        this_cohort_col, alignment_cohort_col = (1, 0)
    elif args.alignment_cohort_col == 'B':
        this_cohort_col, alignment_cohort_col = (0, 1)

    assert args.alignment_file, "Must provide an alignment CSV with --alignment-file"
    alignments = {}
    with open(args.alignment_file) as csvfile:
        line_count = 0
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            line_count += 1
            if line_count == 1 or not row[this_cohort_col] or not row[alignment_cohort_col]:
                continue
            elif alignments.get(row[this_cohort_col]):
                alignments[row[this_cohort_col]].append(row[alignment_cohort_col])
            else:
                alignments[row[this_cohort_col]] = [row[alignment_cohort_col]]
    return alignments


def run(args):
    assert args.cohort_name is not None, "Missing --cohort-name"
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    alignments = {}
    alignment_cohort = None
    if True:  # I believe all cohorts will be aligned with others
        assert args.alignment_cohort_col in ('A', 'B'), "--alignment-cohort-col must be specified (column A or B)"
        alignment_cohort = session.query(Cohort).filter(Cohort.name == args.alignment_cohort_name).first()
        assert alignment_cohort is not None, "Could not find alignment cohort (--alignment-cohort-name) '{}'".format(args.alignment_cohort_name)
        assert cohort != alignment_cohort, "Alignment cohort must be different from cohort"
        alignments = build_alignment_dict(args)

    last_queried_id = args.starting_entity_id or 0
    while last_queried_id is not None:
        sql = session.query(CohortCompound).filter(
            CohortCompound.id > last_queried_id,
            CohortCompound.cohort_id == cohort.id,
        ).order_by(
            CohortCompound.id.asc()
        ).limit(args.index_batch_size or DEFAULT_BATCH_SIZE)
        metabolites = sql.all()
        es_inserts = [
            {
                "_index": INDEX_NAME,
                "_type": DOC_TYPE,
                "_id": cohort.name + "_" + str(metabolite.id),  # careful when changing this
                "_source": {
                    "cohort": cohort.name,
                    "cross_variation": metabolite.cross_variation,
                    "local_ID": metabolite.local_compound_id,
                    "method": cohort.method,
                    "source": cohort.source(),
                    "ML_score": metabolite.ml_score,
                    "MZ": metabolite.mz,
                    "RT": metabolite.rt,
                    "alignment": [
                        {'cohort': alignment_cohort.name, 'local_ID': local_ID}
                        for local_ID
                        in (alignments.get(metabolite.local_compound_id) or [])
                    ]
                }
            }
            for metabolite in metabolites
        ]
        last_queried_id = metabolites[-1].id if len(metabolites) else None
        if args.verbose:
            print "Inserting {} {} documents for {}.  Up to {}.id {}".format(
                len(metabolites),
                args.index,
                cohort.name,
                CohortCompound.__tablename__,
                last_queried_id,
            )
        helpers.bulk(es, es_inserts)
