from fastapi import UploadFile
from typing import List
import json
import os

from model.dataset import Dataset
from service.elasticsearch_client import (
    index_by_doc,
    search_by_query,
    delete_by_id,
)
from config.constants import (
    ELASTICSEARCH_DATABASE_INDEX,
)


def _get_dataset_from_es_result(result) -> Dataset:
    data: Dataset = Dataset.model_validate(result["_source"])
    data["_id"] = result["_id"]
    return data


def get_dataset_by_id(id: str) -> Dataset:
    result = search_by_query(ELASTICSEARCH_DATABASE_INDEX, query={"_id": id})
    if result is not None:
        return _get_dataset_from_es_result(result)
    return None


def get_datasets() -> List[Dataset]:
    data_list: List[Dataset] = []
    results = search_by_query(ELASTICSEARCH_DATABASE_INDEX)
    for result in results:
        data_list.append(_get_dataset_from_es_result(result))
    return data_list


def upload_file_to_dataset(file: UploadFile) -> Dataset:
    contents = file.file.read()
    json_data = json.loads(contents.decode("utf-8"))

    # Validate the correct fields for dataset before saving
    dataset: Dataset = Dataset.model_validate(json_data)

    dataset_id = index_by_doc(ELASTICSEARCH_DATABASE_INDEX, json_data)
    return dataset_id


def delete_dataset_by_id(id: str) -> Dataset:
    response = delete_by_id(ELASTICSEARCH_DATABASE_INDEX, id)
    return response
