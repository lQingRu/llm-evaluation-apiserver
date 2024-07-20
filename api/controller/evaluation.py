from fastapi import APIRouter, HTTPException

from model.api_request import (
    GroundtruthEvaluationRequest,
    DeepEvalRequest,
    LLMJudgeEvaluationRequest,
)
from service.citation_evaluation_service import citation_groundtruth_evaluation
from service.deepeval_service import deepeval_evaluate
from service.llm_judge_service import llm_judge_evaluate

router = APIRouter()


@router.post("/evaluation/groundtruth/custom")
def evaluate_groundtruth_custom(request: GroundtruthEvaluationRequest):
    request: GroundtruthEvaluationRequest = GroundtruthEvaluationRequest.model_validate(
        request
    )
    return citation_groundtruth_evaluation(request.groundtruth, request.answer)
    # try:
    #     request: GroundtruthEvaluationRequest = (
    #         GroundtruthEvaluationRequest.model_validate(request)
    #     )
    #     return citation_groundtruth_evaluation(request.groundtruth, request.answer)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Failed to evaluate: {str(e)}")


@router.post("/evaluation/deepeval")
def evaluate_deepeval(request: DeepEvalRequest):
    return deepeval_evaluate(
        model=request.model,
        metrics_config=request.metrics,
        eval_body=request.evaluation_content,
    )


@router.post("/evaluation/llm-judge")
def evaluate_llm_judge(request: LLMJudgeEvaluationRequest):
    return llm_judge_evaluate(
        question=request.question,
        context=request.context,
        answer=request.answer,
        eval_config=request.eval_config,
    )
