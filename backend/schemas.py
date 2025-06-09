from pydantic import BaseModel, Field
from typing import Optional, List


class ModelMeta(BaseModel):
    id: str = Field(
        ...,
        description="The model ID, e.g., 'mistral:7b-instruct-v0.3-q3_K_M'",
    )
    name: str = Field(..., description="Human-readable model name")


class InputOptions(BaseModel):
    temperature: Optional[float] = 0.7
    num_ctx: Optional[int] = 4096
    seed: Optional[int] = 42
    top_p: Optional[float] = 0.95
    # Add more Ollama generation settings here as needed


class InputData(BaseModel):

    user_message: str = Field(
        ...,
        description="Instruction or natural language question from the user",
    )
    source_code: str = Field(
        ..., description="Source code to be analyzed or processed"
    )
    system_message: Optional[str] = Field(
        default="You are a helpful assistant. Answer in Markdown.",
        description="System-level instruction for the LLM",
    )
    options: InputOptions = Field(default_factory=InputOptions)


class PromptData(BaseModel):
    model: ModelMeta
    input: InputData
    token_count: Optional[int] = None
    token_count_estimated: Optional[bool] = None
    rag_prompt: Optional[str] = None
    rag_sources: Optional[List[str]] = None
    ccc_complexity: Optional[int] = Field(
        None, description="Cognitive Code Complexity (CCC) of the input code"
    )


class OutputData(BaseModel):
    markdown: str = Field(..., description="LLM response in Markdown")
    code: Optional[str] = Field(
        None, description="Cleaned code extracted from the response, if any"
    )
    tokens_used: Optional[int] = Field(
        None, description="Token count used for the request"
    )
    syntax_valid: Optional[bool] = Field(
        None, description="Whether the extracted code is syntactically valid"
    )
    ccc_complexity: Optional[int] = Field(
        None, description="Cognitive Code Complexity (CCC) of the output code"
    )


class TimingData(BaseModel):
    loading_time: float = Field(
        ..., description="Time to load/start model container"
    )
    generation_time: float = Field(
        ..., description="Time to complete the response generation"
    )


class ResponseData(BaseModel):
    model: ModelMeta
    output: OutputData
    timing: TimingData
