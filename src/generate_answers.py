import json
import requests
import base64

# Fill out before running to point to your solution's api
api_url = ""
token_url = ""
client_id = ""
client_secret = ""

def get_auth_token():
    # Encode the client ID and client secret
    authorization = base64.b64encode(
        bytes(client_id + ":" + client_secret, "ISO-8859-1")
    ).decode("ascii")
    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "scope": f"openid {client_id}/.default",
        },
        headers={
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    return response.json()["access_token"]


token = get_auth_token()
def call_chat_api(message: str):
    resp = requests.post(
        api_url,
        json={
            "message": message
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
    )
    resp_body = resp.json()
    print(resp_body)
    # This endpoint returns the entire conversation, so just
    # get the last message from it. That is the answer to what we sent in.
    last_message = resp_body["chat"][-1]
    return last_message

def multiple_choice():
    with open('multiple_choice_questions.json', 'r') as multiple_choice_questions_file:
        questions: list = json.load(multiple_choice_questions_file)

    for question in questions:
        print(question)
        answer_options = "\n".join([f"{option['key']}:{option['option']}" for option in question["options"]])
        message = f"""{question['question']}

        {answer_options}

        Only respond with the letter of the answer you choose. Do not incude the actual text of the answer.
        For instance, if the answer was "B. The Lienholder". You should only respond with "B".
        If you do not know the answer, respond with "Z".
        If you respond with more than 1 character as your response, you will be penalized."""

        generation = call_chat_api(message)
        answer = generation["message"].strip()
        if(len(answer) > 1):
            truncated_answer = answer[0]
            print(f"Invalid resp found.  Translating \"{answer}\" to \"{truncated_answer}\"")
            answer = truncated_answer
        question["answer"] = answer
        # We would normally add the contexts used in our answer to this
        # data as well, but this endpoint currently does not return that.
        # question["contexts"] = [doc["_source"]["content"] for doc in generation["docs"]]

    json_object = json.dumps(questions, indent=4)
    with open("data/multiple_choice_answers.json", "w") as outfile:
        outfile.write(json_object)

def open_ended():
    with open('open_ended_questions.json', 'r') as questions_file:
        questions: list = json.load(questions_file)

    for question in questions:
        print(question)
        generation = call_chat_api(question["question"])
        question["answer"] = generation["message"]
        # We would normally add the contexts used in our answer to this
        # data as well, but this endpoint currently does not return that.
        # question["contexts"] = [doc["_source"]["content"] for doc in generation["docs"]]

    json_object = json.dumps(questions, indent=4)
    # Write this specifically into our ragas folder, as we need to be able to
    # target a folder for loading our ragas dataset.
    with open("data/ragas/open_ended_answers.json", "w") as outfile:
        outfile.write(json_object)

multiple_choice()
open_ended()