import asyncio
import uuid
import torch
import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.storage import save_response

model = None
tokenizer = None

MODEL_NAME = "Qwen/Qwen3-1.7B"


def load_model():
    global model, tokenizer
    if model is None or tokenizer is None:
        print("[INFO] Loading Qwen model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, trust_remote_code=True
        ).eval()
        try:
            model = model.to("cuda" if torch.cuda.is_available() else "cpu")
        except RuntimeError as e:
            print(f"[WARN] Could not use CUDA, using CPU instead: {e}")
            model = model.to("cpu")


def generate_transaction_id() -> str:
    return str(uuid.uuid4())


async def process_prompt_async(transaction_id: str, prompt: str):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, sync_qwen_response, prompt)
    save_response(transaction_id, result)


def sync_qwen_response(prompt: str) -> str:
    load_model()

    start = datetime.datetime.now()
    messages = [{"role": "user", "content": prompt}]
    input_ids = tokenizer.apply_chat_template(
        messages, return_tensors="pt", enable_thinking=False
    )
    input_ids = input_ids.to(model.device)
    output = model.generate(input_ids, max_new_tokens=2000, do_sample=True)
    response = tokenizer.decode(
        output[0][input_ids.shape[1] :],
        skip_special_tokens=True,
        strip_special_tokens=True,
    )
    print(f"prompt finished in {datetime.datetime.now() - start}")
    return extract_model_reply(response)


def extract_model_reply(response: str) -> str:
    if "assistant" in response:
        return response.split("assistant")[-1].strip()
    return response.strip()
