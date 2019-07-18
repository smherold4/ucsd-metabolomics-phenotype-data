import csv
from models import Study, Cohort, CohortCompound
from db import db_connection

COLUMNS = {
  'local_compound_id': 0,
  'mz': 1,
  'rt': 2,
  'cross_variation': 8,
  'ml_score': 9,
}

def validate_args(args):
  assert args.study_id or args.study_name, 'Missing --study-id or --study-name'
  assert args.method in Cohort.METHODS, 'Invalid study method (--method) provided. Must be one of: {}'.format(Cohort.METHODS)
  assert args.units in Cohort.UNITS, 'Invalid units provided. Must be one of: {}'.format(Cohort.METHODS)

def run(args):
  validate_args(args)
  session = db_connection.session_factory()
  study = None
  if args.study_id:
    study = session.query(Study).get(args.study_id)
    assert study is not None, "Could not find study with id {}".format(args.study_id)
  elif args.study_name:
    study = session.query(Study).filter(Study.name==args.study_name).first()
    assert study is not None, "Could not find study with name '{}'".format(args.study_name)

  cohort = session.query(Cohort).filter(Cohort.study_id==study.id, Cohort.method==args.method, Cohort.units==args.units).first()
  assert cohort is None, "A cohort with these parameters (study, method, units) already exists"
  cohort = Cohort(study, args.method, args.units)
  session.add(cohort)
  session.commit()
  
  with open(args.file) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
      line_count += 1
      if line_count == 1:
        continue
      local_compound_id = row[COLUMNS['local_compound_id']]
      cross_variation = row[COLUMNS['cross_variation']] or None
      ml_score = row[COLUMNS['ml_score']] or None
      cohort_compound = CohortCompound(cohort, local_compound_id, cross_variation, ml_score)
      session.add(cohort_compound)
      session.commit()

