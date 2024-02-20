import json

with open("data/multiple_choice_answers.json", "r") as multiple_choice_questions_file:
    multiple_choice_answers: list = json.load(multiple_choice_questions_file)

correct = 0
for answer in multiple_choice_answers:
    if answer["correct_answer"] == answer["answer"]:
        correct += 1

percentage_correct = correct/len(multiple_choice_answers) * 100
print(f"Percentage Correct: {percentage_correct}")