import argparse
from scripts.elasticsearch import manage_subjects_index
from dotenv import load_dotenv
load_dotenv()

INDICES = ['subjects']
ACTIONS = ['create', 'put_settings', 'put_mapping', 'delete', 'populate']


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
        '--file',
        type=str,
        help="Path to phenotype data file")
    parser.add_argument(
        '--cohort-name',
        type=str,
        help="Name of cohort - when ingesting description")
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=False,
        help="Show status outputs to monitor progress of script")
    return parser.parse_args()


if __name__ == '__main__':
    clargs = get_command_line_args()
    assert clargs.index in INDICES, 'Unknown index (--index) provided. Must be one of: {}'.format(
        INDICES)
    assert clargs.action in ACTIONS, 'Unknown action. Must be one of: {}'.format(
        ACTIONS)

    if clargs.index == 'subjects':
        manage_subjects_index.run(clargs)
    else:
        raise Exception('Script is confused')
