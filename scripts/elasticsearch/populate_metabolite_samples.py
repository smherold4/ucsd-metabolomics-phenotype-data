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

es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')], timeout=300)
INDEX_NAME = 'metabolite_samples'
DOC_TYPE = 'metabolite_sample'
DEFAULT_BATCH_SIZE = 40000


def run(args):
    assert args.cohort_name is not None, "Missing --cohort-name"
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    Measurement = measurement_class_factory(cohort)
    line_count = 0
    normalization_by_dataset_id = {(d.id): d.units
                                   for d
                                   in session.query(Dataset).filter(Dataset.cohort == cohort).all()}
    metabolites_by_id = {(c.id): {"local_compound_id": c.local_compound_id, "ml_score": c.ml_score, "mz": c.mz, "rt": c.rt, "method": c.method }
                         for c
                         in session.query(CohortCompound).filter(CohortCompound.cohort == cohort).all()}
    last_queried_id = args.starting_entity_id or 0
    while last_queried_id is not None:
        sql = session.query(Measurement).filter(
            Measurement.id > last_queried_id,
        ).join(
            Measurement.sample,
        ).join(
            Subject, Sample.subject_id == Subject.id, isouter=True,
        ).with_entities(
            Measurement.id,
            Measurement.dataset_id,
            Measurement.measurement,
            Measurement.cohort_compound_id,
            Sample.cohort_id,
            Sample.sample_barcode,
            Sample.plate_well,
            Subject.local_subject_id,
        ).order_by(
            Measurement.id.asc()
        ).limit(args.index_batch_size or DEFAULT_BATCH_SIZE)
        mmts = sql.all()
        es_inserts = [
            {
                "_index": INDEX_NAME,
                "_type": DOC_TYPE,
                "_id": cohort.name.replace(" ", "_") + "_" + str(mmt.id),
                "_source": {
                    "created": datetime.now().strftime("%s"),
                    "measurement": mmt.measurement,
                    "normalization": normalization_by_dataset_id[mmt.dataset_id],
                    "method": metabolites_by_id[mmt.cohort_compound_id]["method"],
                    "local_ID": metabolites_by_id[mmt.cohort_compound_id]["local_compound_id"],
                    "ML_score": metabolites_by_id[mmt.cohort_compound_id]["ml_score"],
                    "MZ": metabolites_by_id[mmt.cohort_compound_id]["mz"],
                    "RT": metabolites_by_id[mmt.cohort_compound_id]["rt"],
                    "plate_well": mmt.plate_well,
                    "sample_barcode": mmt.sample_barcode,
                    "study": cohort.name,
                    "subject": mmt.local_subject_id,
                }
            }
            for mmt in mmts if mmt.cohort_id == cohort.id
        ]
        last_queried_id = mmts[-1].id if len(mmts) else None
        print "Inserting {} {} documents for {}.  Up to {}.id {}".format(
            len(es_inserts),
            args.index,
            cohort.name,
            Measurement.__tablename__,
            last_queried_id,
        )
        for success, info in helpers.parallel_bulk(es, es_inserts):
            if not success:
                print('Parallel bulk failure:', info)
                raise Exception(info)
