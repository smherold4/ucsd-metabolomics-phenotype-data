from scripts import description_ingestion, measurements_ingestion
from models import Cohort
import argparse
from dotenv import load_dotenv
load_dotenv()


MODES = ['description_ingestion', 'measurements_ingestion']


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
        '--method',
        type=str,
        required=True,
        help="Method used in cohort: {}" %
        Cohort.METHODS)
    parser.add_argument(
        '--units',
        type=str,
        required=True,
        help="Units used in cohort: {}" %
        Cohort.UNITS)
    parser.add_argument(
        '--study-name',
        type=str,
        required=True,
        help="Name of study - when ingesting description")
    parser.add_argument(
        '--skip-alignment',
        action='store_true',
        default=False,
        help="Skip alignment and immediately create new compounds - when ingesting description")
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=False,
        help="Show status outputs to monitor progress of script")
    parser.add_argument(
        '--alignment-file',
        type=str,
        help="Path to alignment file")
    parser.add_argument(
        '--alignment-cohort-study',
        type=str,
        help="Name of study of cohort with which to align")
    parser.add_argument(
        '--alignment-cohort-column',
        type=str,
        help="Column ('A' or 'B') of cohort with which we're aligning")

    return parser.parse_args()


if __name__ == '__main__':
    clargs = get_command_line_args()
    assert clargs.method in Cohort.METHODS, 'Invalid study method (--method) provided. Must be one of: {}'.format(
        Cohort.METHODS)
    assert clargs.units in Cohort.UNITS, 'Invalid units provided. Must be one of: {}'.format(
        Cohort.UNITS)

    if clargs.mode == 'description_ingestion':
        description_ingestion.run(clargs)
    elif clargs.mode == 'measurements_ingestion':
        measurements_ingestion.run(clargs)
    else:
        raise Exception('Unknown --mode {}'.format(args.mode))
