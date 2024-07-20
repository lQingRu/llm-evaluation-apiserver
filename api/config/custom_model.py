from deepeval.models.base_model import DeepEvalBaseLLM

from llama_cpp import LlamaGrammar, Llama

GRAMMAR_FILE_PATH = "./local_config/json.gbnf"
MODEL_DIR = "./local_config/gguf_models"


# TODO: Externalize ctx length etc
# Referenced: https://christophergs.com/blog/running-open-source-llms-in-python#select
class CustomModel(DeepEvalBaseLLM):
    def __init__(self, model):
        self.model = model

    def load_model(self):
        return self.model

    # NOTE: Important to ensure json output, see https://docs.confident-ai.com/docs/guides-using-custom-llms#json-confinement-libraries
    def load_grammar(self) -> LlamaGrammar:
        file_path = GRAMMAR_FILE_PATH
        with open(file_path, "r") as handler:
            content = handler.read()
        return LlamaGrammar.from_string(content)

    def generate(self, prompt: str) -> str:
        model = self.load_model()
        response = model.create_completion(
            prompt, max_tokens=256, grammar=self.load_grammar()
        )

        return response["choices"][0]["text"]

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return "Custom Model"


def get_custom_model(model_name: str) -> CustomModel:
    import os

    model_filename = os.path.join(MODEL_DIR, model_name + ".gguf")
    llm = Llama(
        model_path=model_filename,  # path to GGUF file
        n_ctx=2000,  # The max sequence length to use - note that longer sequence lengths require much more resources
        n_threads=4,  # The number of CPU threads to use, tailor to your system and the resulting performance
        n_gpu_layers=0,  # The number of layers to offload to GPU, if you have GPU acceleration available. Set to 0 if no GPU acceleration is available on your system.
    )
    return CustomModel(model=llm)
