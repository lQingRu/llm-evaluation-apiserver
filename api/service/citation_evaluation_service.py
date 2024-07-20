from model.dataset import GroundTruthDataset
from service.citation_groundtruth_service import (
    compare_ground_truth,
    calculate_ground_truth_scores,
)
from model.evaluation import CitationEvaluationResult


def citation_groundtruth_evaluation(data: GroundTruthDataset, answer: str):
    citation_evaluation = compare_ground_truth(answer, data)
    ground_truth_score = calculate_ground_truth_scores(citation_evaluation)
    evaluation_result = CitationEvaluationResult(
        citation_evaluation=citation_evaluation,
        ground_truth_score=ground_truth_score,
        ground_truth_dataset=data,
        candidate_answer_with_citation=answer,
    )
    return evaluation_result
