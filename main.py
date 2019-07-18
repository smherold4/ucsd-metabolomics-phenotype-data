from dotenv import load_dotenv
load_dotenv()

import argparse

from models import Cohort
from scripts import description_ingestion

FILE_TYPES = ['description', 'compound_alignment', 'measurements']

def get_command_line_args():
  parser = argparse.ArgumentParser(description='Move CSV data into Postgres')
  parser.add_argument('--file-type', required=True, type=str, help="Type of file: {}" % FILE_TYPES)
  parser.add_argument('--file', required=True, type=str, help="Path to input file")
  parser.add_argument('--method', type=str, help="Method used in cohort: {}" % Cohort.METHODS)
  parser.add_argument('--units', type=str, help="Units used in cohort: {}" % Cohort.UNITS)
  parser.add_argument('--study-id', type=int, help="Id of study - when processing description")
  parser.add_argument('--study-name', type=str, help="Name of study - when processing description")
  parser.add_argument('--cohort-id', type=int, help="Id of cohort - when processing measurements")

  return parser.parse_args()

if __name__ == '__main__':
  clargs = get_command_line_args()
  assert clargs.file_type in FILE_TYPES, "File type '{}' must be one of the following: {}".format(clargs.file_type, FILE_TYPES)
  if clargs.file_type == 'description':
    description_ingestion.run(clargs)
