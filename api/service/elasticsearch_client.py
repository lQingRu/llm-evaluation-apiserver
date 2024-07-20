from elasticsearch import Elasticsearch
import os
import ast
from config.constants import (
    ELASTICSEARCH_USERNAME,
    ELASTICSEARCH_URL,
    ELASTICSEARCH_SSL_VERIFY,
    ELASTICSEARCH_PASSWORD,
)

es_client = Elasticsearch(
    basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    verify_certs=ast.literal_eval(ELASTICSEARCH_SSL_VERIFY),
    hosts=ELASTICSEARCH_URL,
)


def index_by_doc(index_name: str, doc: dict):
    resp = es_client.index(index=index_name, document=doc)
    if resp["result"] == "created":
        return resp["_id"]
    return None


def delete_by_id(index_name: str, id: str):
    resp = es_client.delete(index=index_name, id=id)
    print(resp)
    return None


def search_by_query(index_name: str, query: dict = None):
    if query != None:
        resp = es_client.search(index=index_name, query=query)
    else:
        resp = es_client.search(index=index_name)
    return resp["hits"]["hits"]
