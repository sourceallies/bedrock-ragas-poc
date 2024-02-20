# Bedrock RAGAS Poc

Notebook to show how to use RAGAS to evaluate RAG solutions, specifically using Bedrock as the backend evauating model instead of OpenAI.

## Setup

You may need to spin up a python virtual env and run against that kernel if you are running locally.  If so, you also may need to activate that kernel and run `pip install ipykernel` to be able to run the notebook cells.

If using the scripts described beolow as well, it may be easier to just use poetry, and run against that kernel when you run the notebook. To do this, simply run `poetry install`.

# Everything that is NOT the notebook

Inside the source folder you will find some scripts using the techniques from the notebook to generate answers and evals based on your solutions API. Below are details on how to do that.

# Example of using some evals against your RAG solution's API

We are performing two different evaluations here.  One against multiple choice questions, and one against open ended questions.

To produce scores for both types, do these steps in order:

1. Add/update your questions in both `src/open_ended_questions.json` and `src/multiple_choice_questions.json`.
2. Run`generate_answers` - Will generate json documents with the answer data included for both types of questions. These will end up in your `src/data` folder
    - You will need to set some values to point to your API and authenticate in the script
3. Run `eval_multiple_choice` - Will print out an accuracy score for your multiple choice answers.
4. Run `eval_open_ended` - Will use RAGAS to generate and print out an accuracy score for your open ended answers.
    - You will need to configure your aws profile before hand. Script is currently using "dev" as the profile, feel free to change it.