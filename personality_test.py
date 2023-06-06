from flask import Flask, render_template, request, redirect, url_for
import webbrowser
import os
import random

#Import the questionnaries
import questionnaries.NEOPIR as NEOPIR
import questionnaries.MiniIPIP as MiniIPIP


app = Flask(__name__)


# Default values (these will be modified with the answers of the first page with options)
questions = MiniIPIP.questions
user_name = None

questionnaires = ["Mini-IPIP", "NEO-PI-R"]


trait_scores = {
    "Openness": {"score": 0, "max_score": 0, "min_score": 0},
    "Conscientiousness": {"score": 0, "max_score": 0, "min_score": 0},
    "Extraversion": {"score": 0, "max_score": 0, "min_score": 0},
    "Agreeableness": {"score": 0, "max_score": 0, "min_score": 0},
    "Neuroticism": {"score": 0, "max_score": 0, "min_score": 0}
}


responses = [
    "1",
    "2",
    "3",
    "4",
    "5"
] 


def process_answer(question):
    global trait_scores

    selected_response = request.form.get('response')
    trait, question, value = questions[question]
    trait_scores[trait]["score"] += int(selected_response) * value
    trait_scores[trait]["max_score"] += max(5 * value, 1 * value)
    trait_scores[trait]["min_score"] += min(5 * value, 1 * value)


def save_results():
    if user_name == None or user_name == "": 
        name = "Anonym"
    else:
        name = user_name
    path = "results/"
    if not os.path.exists(path):
        os.makedirs(path)
    f = open("results/results.txt", "a")

    f.write(f'{user_name}\n')
    f.write('*****************************\n\n')
    f.write("Results on a scale of -1 to 1\n")
    f.write('-----------------------------\n')
    for trait, score in trait_scores.items():
        min_value = score["min_score"]
        max_value = score["max_score"]
        normalized_value = 2 * (score["score"] - min_value) / (max_value - min_value) - 1
        f.write(f'{trait}: {round(normalized_value, 2)}\n')
    f.write('\n')

    f.write("Results on a scale of 0 to 1\n")
    f.write('-----------------------------\n')
    for trait, score in trait_scores.items():
        min_value = score["min_score"]
        max_value = score["max_score"]
        normalized_value = (score["score"] - min_value) / (max_value - min_value)
        f.write(f'{trait}: {round(normalized_value, 2)}\n')
    f.write('\n\n\n')


def process_options(questionnaire, shuffle, name):
    global questions
    global user_name
    
    # questionnaire option
    if questionnaire == "Mini-IPIP": 
        questions = MiniIPIP.questions
    elif questionnaire == "NEO-PI-R":
        questions = NEOPIR.questions

    # Shuffle questions option
    if shuffle == "Yes":
        random.shuffle(questions)

    # User name input
    user_name = name


@app.route('/questions', methods=['GET', 'POST'])
def personality_test():
    if request.method == 'GET':
        # Show the first question
        question_index = 0
        return render_template('personality_test.html', question=questions[question_index][1], question_index=question_index, responses=responses)
        
    else:
        question_index = int(request.form.get('question_index', 0))

        # Process user's response
        process_answer(question_index)

        # Move to the next question or show the result
        if question_index < len(questions) - 1:
            question_index += 1
            return render_template('personality_test.html', question=questions[question_index][1], question_index=question_index, responses=responses)
        else:
            #Save results
            save_results() 
            return 'Test completed!'


@app.route('/', methods=['GET', 'POST'])
def options():
    if request.method == 'GET':
        return render_template('options.html', questionnaires=questionnaires)
        
    else:
        # Process options
        questionnaire = request.form.get('questionnaire')
        shuffle = request.form.get('shuffle')
        name = request.form.get('name')
        process_options(questionnaire, shuffle, name)
        
        # Procesar los datos
        # Redirect to the questionnaire
        return redirect(url_for('personality_test'))
            

if __name__ == '__main__':
    # Open the link in the default web browser
    webbrowser.open("http://127.0.0.1:5000")

    app.run()
    