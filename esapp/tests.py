from django.test import TestCase
from unittest import mock

from esapp.els import (insert, get_docs, update, delete)


class ElasticSearchTest(TestCase):
    def setUp(self):
        self.documents = {
            "hits": {
                "hits": [
                    {
                        "_index": "fs_metadata_1616728615.451842",
                        "_type": "_doc",
                        "_id": "123",
                        "_score": 1.0,
                        "_source": {
                            "size": 100,
                            "created_at": "2021-02-11 05:41:46.969523",
                            "modified_at": "2021-02-11 05:38:49.313844",
                            "ext": "txt"
                        }
                    },
                    {
                        "_index": "fs_metadata_16167286123.11242",
                        "_type": "_doc",
                        "_id": "567",
                        "_score": 1.0,
                        "_source": {
                            "size": 16339,
                            "created_at": "2021-02-11 05:41:46.969523",
                            "modified_at": "2021-02-11 05:38:49.313844",
                            "ext": "csv"
                        }
                    }
                ]
            }
        }

    @mock.patch('elasticsearch.Elasticsearch.index')
    def test_insert_doc_success(self, mock_es):
        doc = self.documents['hits']['hits'][0]['_source']
        mock_es.return_value = {'_id': '123'}
        _id, message, status = insert(doc, _id='123')
        self.assertEqual(_id, '123')
        self.assertEqual(message, 'doc inserted!')
        self.assertEqual(status, 202)

    @mock.patch('elasticsearch.Elasticsearch.search')
    def test_get_docs_success(self, mock_es):
        expected_docs = [doc['_source']
                         for doc in self.documents['hits']['hits']]
        mock_es.return_value = self.documents
        documents, message, status = get_docs()
        self.assertEqual(documents, expected_docs)
        self.assertEqual(message, 'request success')
        self.assertEqual(status, 200)

    @mock.patch('elasticsearch.Elasticsearch.index')
    @mock.patch('elasticsearch.Elasticsearch.get')
    @mock.patch('elasticsearch.client.indices.IndicesClient.get_alias')
    def test_update_doc_success(self, mock_es_indices, mock_es_doc, mock_es_idx):
        mock_es_idx.return_value = {'_id': '123'}
        mock_es_doc.return_value = self.documents['hits']['hits'][0]
        mock_es_indices.return_value = {key['_index']: {
            'alias': {}} for key in self.documents['hits']['hits']}
        expected_source = self.documents['hits']['hits'][0]['_source']
        expected_source.update({'tag': 'my-tag'})
        _source, message, status = update('123', 'my-tag')
        self.assertEqual(_source, expected_source)
        self.assertEqual(message, 'doc inserted!')
        self.assertEqual(status, 202)

    @mock.patch('elasticsearch.client.indices.IndicesClient.delete')
    @mock.patch('elasticsearch.Elasticsearch.get')
    @mock.patch('elasticsearch.client.indices.IndicesClient.get_alias')
    def test_delete_doc_success(self, mock_es_indices, mock_es_doc, mock_es_del):
        mock_es_indices.return_value = {key['_index']: {
            'alias': {}} for key in self.documents['hits']['hits']}
        mock_es_doc.return_value = self.documents['hits']['hits'][0]
        mock_es_del.return_value = {'acknowledged': True}
        _id, message, status = delete('123')
        self.assertEqual(_id, '123')
        self.assertEqual(message, 'request success')
        self.assertEqual(status, 200)
