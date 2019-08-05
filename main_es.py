from dotenv import load_dotenv
load_dotenv()
from elasticsearch import Elasticsearch
import argparse, indices, os
es = Elasticsearch([os.getenv('ELASTICSEARCH_CONFIG_URL', 'http://localhost:9200')])
from scripts.elasticsearch import populate_metabolite_samples, populate_metabolite_alignments

INDICES = ['metabolite_samples', 'metabolite_alignments', 'subject_phenotypes']
ACTIONS = ['create', 'delete', 'populate']

def get_command_line_args():
    parser = argparse.ArgumentParser(description='Move SQL data into Elasticsearch')
    parser.add_argument(
        '--index',
        required=True,
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
        '--phenotype-file',
        type=str,
        help="Path to phenotype data file")
    parser.add_argument(
        '--cohort-name',
        type=str,
        help="Name of cohort - when ingesting description")
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
        '--verbose',
        action='store_true',
        default=False,
        help="Show status outputs to monitor progress of script")
    parser.add_argument(
        '--alignment-cohort-name',
        type=str,
        help="Specify cohort name of cohort to which we're doing alignment")
    parser.add_argument(
        '--alignment-file',
        type=str,
        help="Path to file used for cohort alignment")
    parser.add_argument(
        '--alignment-cohort-col',
        type=str,
        help="Column (A or B) of alignment cohort in alignment file.  If B, then this cohort is assumed to be in column A")
    return parser.parse_args()


if __name__ == '__main__':
    clargs = get_command_line_args()
    assert clargs.index in INDICES, 'Unknown index (--index) provided. Must be one of: {}'.format(
        INDICES)
    assert clargs.action in ACTIONS, 'Unknown action. Must be one of: {}'.format(
        ACTIONS)

    if clargs.action == 'create':
        print es.indices.create(index=clargs.index, body= getattr(indices, clargs.index).index)
    elif clargs.action == 'delete':
        print es.indices.delete(index=clargs.index)
    elif clargs.action == 'populate':
        getattr(__import__(__name__), 'populate_{}'.format(clargs.index)).run(clargs)
    else:
        raise Exception('Script is confused')
