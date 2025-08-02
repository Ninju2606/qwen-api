# QWen API

This project provides an API for executing prompts on the QWen LLM.
Therefore the post route `/handle` takes a prompt and returns a `transaction_id`.
The second get route `/response` provides the result to a given `transaction_id` if present.

Theoretically it is possible to run any other LLM than QWen with this project.
In order to do so the constant `MODEL_NAME` in `processor.py` needs to be replaced by any model listed on https://huggingface.co/models.

## Deployment
To run this service first all requirements need to be installed with `pip install -r .\requirements.txt`.
Afterwards with `uvicorn app.main:app` the application can be started.
