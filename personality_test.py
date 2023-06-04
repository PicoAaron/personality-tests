from flask import Flask, render_template, request

#Import the questionnaries
import questionnaries.NEOPIR as NEOPIR
import questionnaries.MiniIPIP as MiniIPIP

app = Flask(__name__)

# Sample questions and responses
questions = MiniIPIP.questions

'''responses = [
    "1. Very inaccurate",
    "2. Moderately inaccurate",
    "3. Neither Accurate Nor Inaccurate",
    "4. Moderately accurate",
    "5. Very accurate"
] 
'''

responses = [
    "1",
    "2",
    "3",
    "4",
    "5"
] 


@app.route('/', methods=['GET', 'POST'])
def personality_test():
    if request.method == 'POST':
        # Process user's response
        # You can store the response in a database or perform any other required actions
        
        # Move to the next question or show the result
        question_index = int(request.form.get('question_index', 0))
        if question_index < len(questions) - 1:
            question_index += 1
            return render_template('personality_test.html', question=questions[question_index][1], question_index=question_index, responses=responses)
        else:
            return 'Test completed!'
    else:
        # Show the first question
        question_index = 0
        return render_template('personality_test.html', question=questions[question_index][1], question_index=question_index, responses=responses)

if __name__ == '__main__':
    app.run(debug=True)