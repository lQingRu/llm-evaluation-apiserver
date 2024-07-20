import uvicorn
from fastapi import FastAPI
from controller import dataset, evaluation
from fastapi.middleware.cors import CORSMiddleware
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--allowed-origins", type=json.loads, default=["*"], help="allowed origins"
)
parser.add_argument(
    "--allowed-methods", type=json.loads, default=["*"], help="allowed methods"
)
parser.add_argument(
    "--allowed-headers", type=json.loads, default=["*"], help="allowed headers"
)
app = FastAPI()
app.include_router(dataset.router)
app.include_router(evaluation.router)

args = parser.parse_args()
app.add_middleware(
    CORSMiddleware,
    allow_origins=args.allowed_origins,
    allow_methods=args.allowed_methods,
    allow_headers=args.allowed_headers,
)


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
