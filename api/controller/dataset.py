from fastapi import APIRouter, UploadFile, HTTPException
from service.dataset_service import (
    upload_file_to_dataset,
    get_datasets,
    delete_dataset_by_id,
    get_dataset_by_id,
)

router = APIRouter()


@router.get("/datasets/")
def get_all_datasets():
    try:
        return get_datasets()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get all datasets: {str(e)}"
        )


@router.get("/datasets/{id}/")
def get_dataset(id: str):
    try:
        return get_dataset_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {str(e)}")


@router.post("/datasets/")
def create_dataset(file: UploadFile):
    try:
        return upload_file_to_dataset(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.delete("/datasets/{id}/")
def delete_dataset(id: str):
    try:
        return delete_dataset_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {str(e)}")
