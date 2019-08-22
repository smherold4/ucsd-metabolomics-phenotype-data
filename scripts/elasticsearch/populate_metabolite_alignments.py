import indices
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from db import db_connection
from models import *
from sqlalchemy.orm import joinedload
from scripts.elasticsearch import alignment_file_params
import sys
import os
import re
import csv

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')], timeout=30)
INDEX_NAME = 'metabolite_alignments'
DOC_TYPE = 'metabolite_alignment'
DEFAULT_BATCH_SIZE = 40000


def build_alignment_dict(args, alignment_params, cohort, session):
    alignments = {}
    for alignment_file in alignment_params:
        alignment_cohort = session.query(Cohort).filter(Cohort.name == alignment_file['cohort_name']).first()
        assert alignment_cohort is not None, "Could not find alignment cohort for {}".format(alignment_file)
        assert cohort != alignment_cohort, "Alignment cohort must be different from cohort for {}".format(alignment_file)
        this_cohort_col, alignment_cohort_col = (None, None)
        if alignment_file['cohort_column'] == 'A':
            this_cohort_col, alignment_cohort_col = (1, 0)
        elif alignment_file['cohort_column'] == 'B':
            this_cohort_col, alignment_cohort_col = (0, 1)
        else:
            raise Exception("Invalid cohort_column (should be A or B) for {}".format(alignment_file))
        with open(alignment_file['path']) as csvfile:
            line_count = 0
            csv_reader = csv.reader(csvfile, delimiter=',')
            for row in csv_reader:
                line_count += 1
                if line_count == 1 or not row[this_cohort_col] or not row[alignment_cohort_col]:
                    continue
                entry = {
                    "local_ID": row[alignment_cohort_col],
                    "study": alignment_cohort.name,
                }
                if alignments.get(row[this_cohort_col]):
                    alignments[row[this_cohort_col]].append(entry)
                else:
                    alignments[row[this_cohort_col]] = [entry]
    return alignments


def run(args):
    assert args.cohort_name is not None, "Missing --cohort-name"
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    Measurement = measurement_class_factory(cohort)
    alignment_params = getattr(alignment_file_params, cohort.name.replace(" ", "_")).files
    alignments = build_alignment_dict(args, alignment_params, cohort, session)


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
                "_id": cohort.name.replace(" ", "_") + "_" + str(metabolite.id),  # careful when changing this
                "_source": {
                    "alignment": (alignments.get(metabolite.local_compound_id) or []),
                    "cross_variation": metabolite.cross_variation,
                    "local_ID": metabolite.local_compound_id,
                    "method": cohort.method,
                    "source": cohort.source(),
                    "ML_score": metabolite.ml_score,
                    "MZ": metabolite.mz,
                    "RT": metabolite.rt,
                    "study": cohort.name,
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
