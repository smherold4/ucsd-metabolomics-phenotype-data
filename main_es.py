from dotenv import load_dotenv
load_dotenv()
from elasticsearch import Elasticsearch
from elasticsearch.client import SnapshotClient
import argparse, indices, os
es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')], timeout=40)
import scripts.elasticsearch as scripts

INDICES = [
    'metabolite_samples',
    'metabolite_alignments',
    'subject_phenotypes',
    'phenotype_descriptions',
    'sample_phenotypes',
    'microbiome_abundances',
    'microbiome_alignments',
    'microbiome_sequences',
]
ACTIONS = ['create', 'delete', 'populate', 'snapshot']

SNAPSHOT_REPOSITORY = 'monthly'


def get_command_line_args():
    parser = argparse.ArgumentParser(description='Move SQL data into Elasticsearch')
    parser.add_argument(
        '--index',
        type=str,
        help="Elasticsearch index: {}" %
        INDICES)
    parser.add_argument(
        '--action',
        type=str,
        required=True,
        help="Action to perform: {}" %
        ACTIONS)
    parser.add_argument(
        '--microbiome-file',
        type=str,
        help="Path to microbiome data")
    parser.add_argument(
        '--phenotype-file',
        type=str,
        help="Path to phenotype data or description file")
    parser.add_argument(
        '--cohort-name',
        type=str,
        help="Name of cohort - when ingesting description")
    parser.add_argument(
        '--snapshot-name',
        type=str,
        help="Name of snapshot")
    parser.add_argument(
        '--index-batch-size',
        type=int,
        help="Amount of documents to bulk index at once",
    )
    parser.add_argument(
        '--starting-entity-id',
        type=int,
        help="Entity ID from which to start indexing",
    )
    parser.add_argument(
        '--age-at-sample-collection-label',
        type=str,
        default='BL_AGE',
        help="In phenotype CSV, the label of the age_at_sample_collection")
    parser.add_argument(
        '--subject-id-label',
        type=str,
        help="In phenotype CSV, the label of the Subject Id")
    parser.add_argument(
        '--exam-no',
        type=str)
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=False,
        help="Show status outputs to monitor progress of script")
    return parser.parse_args()


if __name__ == '__main__':
    clargs = get_command_line_args()

    assert clargs.action in ACTIONS, 'Unknown action. Must be one of: {}'.format(
        ACTIONS)

    if clargs.action != 'snapshot':
        assert clargs.index in INDICES, 'Unknown index (--index) provided. Must be one of: {}'.format(INDICES)

    if clargs.action == 'snapshot':
        assert clargs.snapshot_name is not None, "Must provide a --snapshot-name"
        es_snapshot = SnapshotClient([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')])
        response = es_snapshot.create(repository=SNAPSHOT_REPOSITORY, snapshot=clargs.snapshot_name, master_timeout=30)
        print(response)
    elif clargs.action == 'create':
        print es.indices.create(index=clargs.index, body=getattr(indices, clargs.index).index)
    elif clargs.action == 'delete':
        print es.indices.delete(index=clargs.index)
    elif clargs.action == 'populate':
        getattr(scripts, 'populate_{}'.format(clargs.index)).run(clargs)
    else:
        raise Exception('Script is confused')
