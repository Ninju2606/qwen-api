from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    transaction_id: str


class ResponseResult(BaseModel):
    transaction_id: str
    response: str | None = None
