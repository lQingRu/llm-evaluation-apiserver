from model.dataset import GroundTruthDataset
from pydantic import BaseModel
from service.deepeval_service import DeepEvalMetricConfig, DeepEvalModel, DeepEvalBody
from typing import List, Optional
from service.llm_judge_service import LLMAsAJudgeEval


class GroundtruthEvaluationRequest(BaseModel):
    groundtruth: GroundTruthDataset
    answer: str


class DeepEvalRequest(BaseModel):
    evaluation_content: DeepEvalBody
    metrics: List[DeepEvalMetricConfig]
    model: DeepEvalModel


class LLMJudgeEvaluationRequest(BaseModel):
    question: str
    context: str
    answer: str
    eval_config: Optional[LLMAsAJudgeEval] = LLMAsAJudgeEval()
