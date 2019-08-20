from dotenv import load_dotenv
load_dotenv()
import argparse
from models import Cohort, Dataset
from scripts.sql import raw_ingestion, key_ingestion

MODES = ['raw_ingestion', 'key_ingestion']

def get_version(clargs):
    if clargs.cohort_name in ['FHS', 'FINRISK']:
        return 'v1'
    else:
        return 'v2'

def get_command_line_args():
    parser = argparse.ArgumentParser(description='Move CSV data into Postgres')
    parser.add_argument(
        '--mode',
        required=True,
        type=str,
        help="Mode of execution: {}" %
        MODES)
    parser.add_argument(
        '--file',
        required=True,
        type=str,
        help="Path to input file")
    parser.add_argument(
        '--csv-chunksize',
        type=int,
    )
    parser.add_argument(
        '--units',
        type=str,
        help="Units used in cohort: {}" %
        Dataset.UNITS)
    parser.add_argument(
        '--cohort-name',
        type=str,
        required=True)
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
    version = get_version(clargs)
    if clargs.mode == 'raw_ingestion':
        getattr(raw_ingestion, version).run(clargs)
    elif clargs.mode == 'key_ingestion':
        getattr(key_ingestion, version).run(clargs)
    else:
        raise Exception('Unknown --mode {}'.format(clargs.mode))
