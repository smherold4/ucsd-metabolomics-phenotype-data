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

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')], timeout=30)
INDEX_NAME = 'metabolite_alignments'
DOC_TYPE = 'metabolite_alignment'
DEFAULT_BATCH_SIZE = 40000

ALIGNMENT_FILE_PATH = '/volume1/Jain Lab Data/MassSpecDatabase/Eicosanoid method/'

def build_alignment_dict(cohort, session):
    alignments = {}
    alignment_regex = r'AlignedPeaks\_([^\_]+)\_([^\_]+)\.csv'
    directory = ALIGNMENT_FILE_PATH + cohort.name
    for filename in os.listdir(directory):
        re_match = re.search(alignment_regex, filename)
        if re_match:
            alignment_cohort = None
            this_cohort_col, alignment_cohort_col = (None, None)
            cohort1, cohort2 = re_match.group(1, 2)
            if cohort.name.upper() == cohort1.upper():
                alignment_cohort = session.query(Cohort).filter( Cohort.name.in_([cohort2, cohort2.upper()]) ).first()
                this_cohort_col, alignment_cohort_col = (0, 1)
            elif cohort.name.upper() == cohort2.upper():
                alignment_cohort = session.query(Cohort).filter( Cohort.name.in_([cohort1, cohort1.upper()]) ).first()
                this_cohort_col, alignment_cohort_col = (1, 0)
            if alignment_cohort:
                print('Building alignments with {}'.format(alignment_cohort.name))
                with open(directory + '/' + filename) as csvfile:
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
    alignments = build_alignment_dict(cohort, session)

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
                    "min_raw": metabolite.min_raw,
                    "max_raw": metabolite.max_raw,
                    "prevalence": metabolite.prevalence,
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
