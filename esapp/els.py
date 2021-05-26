import json
import time

import elasticsearch
from decouple import config

els_host = 'localhost'
els_port = 9200

es = elasticsearch.Elasticsearch(host=els_host, port=els_port)


def insert(_source, _id=None, _index=None):
    """
    Creates new index <fs_metadata_{timestamp}> with _source as document
        in elastic search
    Inserts metadata to this index
    :param _source: metadata dictionary
    :param _id: string
    :param _index: string
    :returns: id, message, status
    """
    message, status = 'doc inserted!', 202
    response = dict()
    timestamp = time.time()
    index = _index if _index else f"fs_metadata_{timestamp}"
    try:
        response = es.index(
            index=index, body=_source, id=_id)
    except Exception as ex:
        message, status = str(ex), 400
    return response.get("_id"), message, status


def get_docs():
    """
    Fetch all documents from all indexes in elastic search
    :param : None
    :returns: documents, message, status  
    """
    message, status = 'request success', 200
    try:
        response = es.search(index="fs_metadata_*",
                             body={"query": {"match_all": {}}})
    except Exception as ex:
        message, status = str(ex), 400
    documents = []
    for res in response['hits']['hits']:
        documents.append(res['_source'])
    return documents, message, status


def update(doc_id, tag):
    """
    Updates document from elastic search having id = doc_id 
    Adds tag to that document
    :param doc_id: string
    :param tag: string
    :returns: _source, message, status
    """
    response = es.indices.get_alias("fs_metadata_*")
    document = dict()
    for index in list(response.keys()):
        try:
            document = es.get(index=index, id=doc_id)
            break
        except elasticsearch.exceptions.NotFoundError as ex:
            pass
    _source = document.get('_source', {})
    _source['tag'] = tag
    _index = document.get('_index')
    _id = document.get('_id')
    _id, message, status = insert(_source=_source, _index=_index, _id=_id)
    return _source, message, status


def delete(doc_id):
    """
    Deletes document from elastic search having id = doc_id 
    :param doc_id: string
    :returns: document_id, message, status
    """
    message, status = 'request success', 200
    document = dict()
    response = es.indices.get_alias("fs_metadata_*")
    for index in list(response.keys()):
        try:
            document = es.get(index=index, id=doc_id)
            if document:
                res = es.indices.delete(index=index, ignore=[400, 404])
                break
        except elasticsearch.exceptions.NotFoundError:
            pass
        except Exception as ex:
            message, status = str(ex), 404
            break
    return document.get('_id'), message, status
