from deepeval import evaluate
from deepeval.metrics import (
    FaithfulnessMetric,
    HallucinationMetric,
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
)
from deepeval.test_case import LLMTestCase
from enum import Enum
from typing import List
from pydantic import BaseModel
from config.custom_model import get_custom_model
from deepeval.metrics import BaseMetric
import asyncio
from config.constants import DEPLOYMENT_ENV


class DeepEvalMetric(Enum):
    # Whether the actual_output factually aligns to the retrieval_context
    FAITHFULNESS = "Faithfulness"
    # Whether the actual_output factually aligns to the context
    HALLUCINATION = "Hallucination"
    # Whether the actual_output is relevant to the input
    RELEVANCY = "Relevancy"
    # Whether the retrieval_context is relevant to the input
    CONTEXTUAL_PRECISION = "Contextual Precision"
    # Whether the retrieval_context aligns to the expected_output
    CONTEXTUAL_RECALL = "Contextual Recall"
    # TODO: Consider G-Eval (COT) for custom metrics: https://docs.confident-ai.com/docs/metrics-llm-evals


class DeepEvalModel(Enum):
    PHI_3_MINI_4K_INSTRUCT_Q4 = "Phi-3-mini-4k-instruct-q4"
    MISTRAL_7B_INSTRUCT_V0_3_Q4 = "Mistral-7B-Instruct-v0.3.Q4_K_M"


class DeepEvalBody(BaseModel):
    input: str  # Question
    actual_output: str  # Generated answer
    retrieval_context: List[str] = None  # Context
    expected_output: str = None  # Needed for [ContextualPrecision, ]
    context: List[str] = None  # Needed for [Hallucination, ]


class DeepEvalMetricConfig(BaseModel):
    metric: DeepEvalMetric
    threshold: float


async def run_evaluation_async(metrics: List[BaseMetric], test_case: LLMTestCase):
    # Execute measurements in parallel
    await asyncio.gather(*[metric.a_measure(test_case) for metric in metrics])


def deepeval_evaluate(
    model: DeepEvalModel,
    metrics_config: List[DeepEvalMetricConfig],
    eval_body: DeepEvalBody,
):

    include_reason = True if DEPLOYMENT_ENV == "DEVT" else False
    verbose_mode = True if DEPLOYMENT_ENV == "DEVT" else False
    eval_model = get_custom_model(model.value)

    # NOTE: async_mode = True only mean that the factual claims and truths (In the context of FaithfulnessMetric) will be executed concurrently. The measurement execution will still be blocking

    metrics_to_eval: List[BaseMetric] = []
    for config in metrics_config:
        match config.metric:
            case DeepEvalMetric.FAITHFULNESS:
                metrics_to_eval.append(
                    FaithfulnessMetric(
                        threshold=config.threshold,
                        model=eval_model,
                        include_reason=include_reason,
                        verbose_mode=verbose_mode,
                    )
                )
            case DeepEvalMetric.HALLUCINATION:
                metrics_to_eval.append(
                    HallucinationMetric(
                        threshold=config.threshold,
                        model=eval_model,
                        include_reason=include_reason,
                        verbose_mode=verbose_mode,
                    )
                )
            case DeepEvalMetric.RELEVANCY:
                metrics_to_eval.append(
                    AnswerRelevancyMetric(
                        threshold=config.threshold,
                        model=eval_model,
                        include_reason=include_reason,
                        verbose_mode=verbose_mode,
                    )
                )
            case DeepEvalMetric.CONTEXTUAL_PRECISION:
                metrics_to_eval.append(
                    ContextualPrecisionMetric(
                        threshold=config.threshold,
                        model=eval_model,
                        include_reason=include_reason,
                        verbose_mode=verbose_mode,
                    )
                )

        test_case = LLMTestCase(
            input=eval_body.input,
            actual_output=eval_body.actual_output,
            retrieval_context=eval_body.retrieval_context,
            expected_output=eval_body.expected_output,
            context=eval_body.context,
        )

    asyncio.run(run_evaluation_async(metrics_to_eval, test_case))
    evaluation_result = evaluate([test_case], metrics_to_eval)
    print("EVALUATION_RESULT: " + str(evaluation_result))
    return evaluation_result
