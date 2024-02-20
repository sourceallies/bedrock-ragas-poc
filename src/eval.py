from ragas import evaluate
from datasets import load_dataset
import os
import langchain
from ragas.llms.prompt import Prompt
from ragas.metrics import answer_correctness
import boto3
from langchain_community.chat_models import BedrockChat
from langchain_community.embeddings import BedrockEmbeddings

langchain.debug = True
os.environ["RAGAS_DO_NOT_TRACK "] = "true"

dataset = load_dataset("./data")
print(dataset)
print(dataset["train"].to_pandas())

boto3.setup_default_session(profile_name="dev")
BEDROCK_CLIENT = boto3.client("bedrock-runtime", "us-east-1")
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1", client=BEDROCK_CLIENT
)
llm = BedrockChat(
    model_id="anthropic.claude-instant-v1",
    model_kwargs={"temperature": 0.1, "max_tokens_to_sample": 1000},
    client=BEDROCK_CLIENT,
)

new_instruction = f"""{answer_correctness.correctness_prompt.instruction}
Generate "Extracted Statements" similar to the {len(answer_correctness.correctness_prompt.examples)} examples I am about to give you.
Respond only in JSON format, just like the "Extracted Statements" in these two examples.
Do not say anything before or after the JSON output, or you will be penalized.
Only generate the data for the last question and ground truth provided."""

bedrock_correctness_prompt = Prompt(
    name="bedrock_correctness_prompt",
    instruction=new_instruction,
    examples=answer_correctness.correctness_prompt.examples,
    input_keys=answer_correctness.correctness_prompt.input_keys,
    output_key=answer_correctness.correctness_prompt.output_key,
    output_type=answer_correctness.correctness_prompt.output_type,
)

results = evaluate(
    dataset['train'],
    llm=llm,
    embeddings=embeddings,
    metrics=[
        answer_correctness
    ]
)

def results_string(dataset):
    return f"""{dataset["answer_correctness"]}  (Invalid Records: {dataset.to_pandas()['answer_correctness'].isnull().sum()}/{len(dataset.dataset)})"""

print(results_string(results))