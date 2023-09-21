# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
import requests
import html

# Create a Flask app instance
app = Flask(__name__)

# Define the API URL and parameters for fetching quiz questions
API_URL = "https://opentdb.com/api.php"
parameter = {
    "amount": 10,       # Number of questions to fetch
    "type": "boolean",  # Type of questions (True/False)
    "category": 18      # Category ID (Change as needed)
}

# Initialize global variables to track quiz progress and score
current_question_index = 0
score = 0

# Define a route for the home page
@app.route('/')
def index():
    global current_question_index
    global score
    global question_data
    
    # Fetch quiz questions from the API
    response = requests.get(API_URL, params=parameter)
    response.raise_for_status()
    data = response.json()
    question_data = data["results"]
    
    # Check if there are more questions to display
    if current_question_index < len(question_data):
        # Increment the question number by 1 since it's 1-based for display
        question_number = current_question_index + 1

        # Get the current question text and unescape it
        question = html.unescape(question_data[current_question_index]["question"])
        
        # Render the quiz template with the current question
        return render_template('quiz.html', question=question, question_number=question_number)
    else:
        # If all questions have been answered, show the quiz completion page
        return render_template('quiz_complete.html', score=score)

# Define a route to handle user answers
@app.route('/answer', methods=['POST'])
def answer():
    global current_question_index
    global score
    
    # Get the user's answer from the form
    user_answer = request.form.get('answer')
    
    # Get the correct answer for the current question
    correct_answer = question_data[current_question_index]["correct_answer"]
    
    # Check if the user's answer is correct and update the score
    if user_answer == "True" and correct_answer or user_answer == "False" and not correct_answer:
        score += 1  # Increment the score if the answer is correct
    
    # Move to the next question
    current_question_index += 1
    
    # Redirect to the next question or quiz completion page
    return redirect(url_for('index'))

# Define a route to start a new quiz
@app.route('/start-quiz')
def start_quiz():
    global current_question_index
    global score
    
    # Reset the quiz state
    current_question_index = 0
    score = 0

    # Redirect to the first question
    return redirect(url_for('index'))

# Run the Flask app if this script is the main program
if __name__ == '__main__':
    app.run(debug=True)
