from indices import subjects
from datetime import datetime
from elasticsearch import Elasticsearch
import sys

es = Elasticsearch()
INDEX_NAME = 'subjects'


def run(args):
    if args.action == 'create_index':
        es.indices.create(index=INDEX_NAME, body=subjects.index)

    # UPDATE DOC_TYPE MAPPINGS
    # es.indices.put_mapping(index=INDEX_NAME, doc_type='dog', body=dogs.index['mappings']['dog'])

    # UPDATE SETTINGS (must close and open index to add analyzers)
    # es.indices.close(index=INDEX_NAME)
    # es.indices.put_settings(index=INDEX_NAME, body=dogs.index['settings'])
    # es.indices.open(index=INDEX_NAME)

    # INSERT/UPDATE DOCS
    # es.index(index=INDEX_NAME, doc_type='dog', id=1, body=dog.buddy)
    # es.index(index=INDEX_NAME, doc_type='dog', id=2, body=dog.tuffy)
    # es.index(index=INDEX_NAME, doc_type='dog', id=3, body=dog.minnie)

    # DELETE DOCS
    # es.delete(index=INDEX_NAME, doc_type='dog', id=1)
    # es.delete(index=INDEX_NAME, doc_type='dog', id=2)

    # UPDATE DOCS
    # es.update(
    #   index=INDEX_NAME,
    #   doc_type='dog',
    #   id='W_uSzmsBUhRInbGHV2mc',
    #   body={'doc': dog.buddy})
