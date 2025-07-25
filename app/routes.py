from fastapi import APIRouter, BackgroundTasks
from app.models import PromptRequest, PromptResponse, ResponseResult
from app.processor import generate_transaction_id, process_prompt_async
from app.storage import save_transaction, get_response, delete_response

router = APIRouter()


@router.post("/handle", response_model=PromptResponse)
async def handle_prompt(request: PromptRequest, background_tasks: BackgroundTasks):
    transaction_id = generate_transaction_id()
    save_transaction(transaction_id)
    background_tasks.add_task(process_prompt_async, transaction_id, request.prompt)
    return PromptResponse(transaction_id=transaction_id)


@router.get("/response", response_model=ResponseResult)
async def get_response_by_id(transaction_id: str):
    result = get_response(transaction_id)
    if result is not None:
        delete_response(transaction_id)
    return ResponseResult(transaction_id=transaction_id, response=result)
