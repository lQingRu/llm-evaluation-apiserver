from pydantic import BaseModel
from typing import List, Dict
import uuid

from utils.text_splitter import split_text_with_citations


class DataDocument(BaseModel):
    id: str = str(uuid.uuid4())
    text: str


class Dataset(BaseModel):
    id: str  # Use auto-generated elasticsearch ID
    docs: List[DataDocument]


class GroundTruthData(DataDocument):
    has_answer: bool


class GroundTruthDataset(BaseModel):
    id: str = str(uuid.uuid4())
    question: str
    answer_with_citation: str
    docs: List[GroundTruthData]

    def get_split_text_citation(self):
        return split_text_with_citations(self.answer_with_citation)[0]

    def get_valid_citations_map(self) -> Dict[str, List[GroundTruthData]]:
        citations_map: Dict[str, List[GroundTruthData]] = dict()
        for doc in self.docs:
            if doc.has_answer:
                citations_map.setdefault(doc.id, []).append(doc)
        return citations_map

    def get_docs_has_answer_map(self) -> Dict[str, bool]:
        has_answer_map: Dict[str, bool] = dict()
        for doc in self.docs:
            has_answer_map[doc.id] = doc.has_answer
        return has_answer_map

    def get_docs_no_answer(self) -> List[GroundTruthData]:
        docs_no_answer: List[GroundTruthData] = []
        for doc in self.docs:
            if doc.has_answer == False:
                docs_no_answer.append(doc)
        return docs_no_answer
