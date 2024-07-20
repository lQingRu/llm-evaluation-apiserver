# evaluation-apiserver

## Pre-requisites

### GGUF models needed for DeepEval

- See `DeepEvalModel` enums in `deepeval_service.py`
- Download GGUF models and store it in `local_config/gguf_models` directory:
  - `Phi-3-mini-4k-instruct-q4.gguf`: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/blob/main/Phi-3-mini-4k-instruct-q4.gguf
  - `Mistral-7B-Instruct-v0.3.Q4_K_M.gguf`: https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF/blob/main/Mistral-7B-Instruct-v0.3.Q4_K_M.gguf

### Environment variables

- See `.env.template`

## TODO

- Persist data
  - Dataset
  - Results
  - Prompt
- Optimize evaluation
- Provide comparison between evaluations
- Provide high-level evaluation
