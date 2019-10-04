from dotenv import load_dotenv
load_dotenv()
import argparse
from models import Cohort, Dataset, CohortCompound
from scripts.sql import measurement_ingestion, key_mapping

MODES = ['measurement_ingestion', 'key_mapping']

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
        '--col-of-first-measurement',
        type=str,
    )
    parser.add_argument(
        '--units',
        type=str,
        help="Units used in cohort: {}" %
        Dataset.UNITS)
    parser.add_argument(
        '--method',
        type=str,
        help="Spectroscopy method used: {}" %
        CohortCompound.METHODS)
    parser.add_argument(
        '--cohort-name',
        type=str,
        required=True)
    parser.add_argument(
        '--exam-no',
        type=str)

    return parser.parse_args()


if __name__ == '__main__':
    clargs = get_command_line_args()
    if clargs.mode == 'measurement_ingestion':
        measurement_ingestion.run(clargs)
    elif clargs.mode == 'key_mapping':
        key_mapping.run(clargs)
    else:
        raise Exception('Unknown --mode {}'.format(clargs.mode))
