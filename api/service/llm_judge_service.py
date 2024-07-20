from typing import List
from pydantic import BaseModel, Field
from langchain_community.llms import HuggingFaceEndpoint
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
import logging
from langchain_core.exceptions import OutputParserException
from config.constants import HUGGINGFACEHUB_API_TOKEN

EVALUATION_PROMPT_TEMPLATE = """
You are an expert judge evaluating the Retrieval Augmented Generation applications. Your task is to evaluate a given answer based on a context and question using the criteria provided below.
 
Evaluation Criteria (Additive Score, 0-5):
{additive_criteria}
 
Evaluation Steps:
{evaluation_steps}

Now, please evaluate the following:
 
Question:
{question}
Context:
{context}
Answer:
{answer}
"""

ADDITIVE_CRITERIA = """1. Context: Award 1 point if the answer uses only information provided in the context, without introducing external or fabricated details.
2. Completeness: Add 1 point if the answer addresses all key elements of the question based on the available context, without omissions.
3. Conciseness: Add a final point if the answer uses the fewest words possible to address the question and avoids redundancy."""

EVALUATION_STEPS = """1. Read provided context, question and answer carefully.
2. Go through each evaluation criterion one by one and assess whether the answer meets the criteria.
3. Compose your reasoning for each critera, explaining why you did or did not award a point. You can only award full points. 
4. Calculate the total score by summing the points awarded."""


class LLMAsAJudgeEval(BaseModel):
    additive_criteria: str = ADDITIVE_CRITERIA
    evaluation_steps: str = EVALUATION_STEPS
    model: str = "mistralai/mixtral-8x7b-instruct-v0.1"  # Huggingface model


class LLMAsAJudgeResponse(BaseModel):
    total_score: int = Field(description="Sum of additive criteria scores (0 to 5)")
    reasoning: str = Field(
        description="Your step-by-step explanation for the Evaluation Criteria, why you awarded a point or not."
    )


def llm_judge_evaluate(
    question: str, context: str, answer: str, eval_config: LLMAsAJudgeEval
):
    llm = HuggingFaceEndpoint(
        repo_id=eval_config.model,
        temperature=0.01,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )

    parser = PydanticOutputParser(pydantic_object=LLMAsAJudgeResponse)

    prompt = PromptTemplate(
        template=EVALUATION_PROMPT_TEMPLATE,
        input_variables=[
            "additive_criteria",
            "evaluation_steps",
            "question",
            "context",
            "answer",
        ],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    try:
        response = chain.invoke(
            {
                "additive_criteria": eval_config.additive_criteria,
                "evaluation_steps": eval_config.evaluation_steps,
                "question": question,
                "context": context,
                "answer": answer,
            }
        )
        return response
    except OutputParserException as parser_exception:
        llm_response = parser_exception.llm_output
        logging.error("OutputParserException: " + str(parser_exception))
        return llm_response
