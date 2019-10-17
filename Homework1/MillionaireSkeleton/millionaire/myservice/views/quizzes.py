from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.quiz import Quiz, Question, Answer, NonExistingAnswerError, LostQuizError, CompletedQuizError

quizzes = JsonBlueprint('quizzes', __name__)

_LOADED_QUIZZES = {}  # list of available quizzes
_QUIZNUMBER = 0  # index of the last created quizzes



@quizzes.route("/quizzes",methods=["POST","GET"])
def all_quizzes():
    if 'POST' == request.method:
        result = create_quiz(request) # Create new quiz 
        
    elif 'GET' == request.method:
        result = get_all_quizzes(request) # Retrieve all loaded quizzes
        

    return result


@quizzes.route("/quizzes/loaded", methods=['GET'])
def loaded_quizzes():  # returns the number of quizzes currently loaded in the system
    global _LOADED_QUIZZES
    return jsonify({"loaded_quizzes":len(_LOADED_QUIZZES)}) # Return the correct number


@quizzes.route("/quiz/<string:id>",methods = ["GET","DELETE"])
def single_quiz(id):
    global _LOADED_QUIZZES
    result = ""

    exists_quiz(id) # check if the quiz is an existing one
    if 'GET' == request.method:  
       
        result = jsonify(_LOADED_QUIZZES[id].serialize())  # retrieve a quiz <id>
       

    elif 'DELETE' == request.method:
        
        # delete a quiz and get back number of answered questions
        # and total number of questions
        quiz = _LOADED_QUIZZES[id] 
        result = jsonify({"answered_questions":quiz.currentQuestion,'total_questions':len(quiz.questions)})
        del _LOADED_QUIZZES[id]
    return result


@quizzes.route("/quiz/<string:id>/question", methods=['GET'])
def play_quiz(id):
    global _LOADED_QUIZZES
    result = ""

    # check if the quiz is an existing one
    exists_quiz(id)
    if 'GET' == request.method:  
        quiz = _LOADED_QUIZZES[id]
        result = ""

        try:
            result = quiz.getQuestion() # retrieve next question in a quiz
        except CompletedQuizError as error:
            result = jsonify({"msg":"completed quiz"}) # the quiz has already been completed
        except LostQuizError as error:
            result = jsonify({"msg":"you lost!"}) # the quiz has been failed
    return result


@quizzes.route("/quiz/<string:id>/question/<answer>", methods=['PUT'])
def answer_question(id, answer):
    global _LOADED_QUIZZES
    result = ""
    
    exists_quiz(id) # check if the quiz is an existing one

    quiz = _LOADED_QUIZZES[id]
    
    try:
        quiz.isOpen() # check if quiz is still open
    
    except LostQuizError: # the quiz <id> has already been failed
        result = "you lost!"
        return jsonify({"msg":result})

    except CompletedQuizError: # the quiz has already been completed
        result = "completed quiz"
        return jsonify({"msg":result})
    
    if 'PUT' == request.method:  

        try:
            quiz.checkAnswer(answer)  # Check answers
            result = quiz.currentQuestion

        except CompletedQuizError: #quiz completed successfully => the user wins!!
            result = "you won 1 million clams!"

        except LostQuizError: # wrong answer => quiz failed!!
            result = "you lost!"

        except NonExistingAnswerError: # the answer doesn't exist...
            result = "non-existing answer!"
        return jsonify({'msg': result})
        

############################################
# USEFUL FUNCTIONS BELOW (use them, don't change them)
############################################

def create_quiz(request):
    global _LOADED_QUIZZES, _QUIZNUMBER

    json_data = request.get_json()
    qs = json_data['questions']
    questions = []
    for q in qs:
        question = q['question']
        answers = []
        for a in q['answers']:
            answers.append(Answer(a['answer'], a['correct']))
        question = Question(question, answers)
        questions.append(question)

    _LOADED_QUIZZES[str(_QUIZNUMBER)] = Quiz(_QUIZNUMBER, questions)
    _QUIZNUMBER += 1

    return jsonify({'quiznumber': _QUIZNUMBER - 1})


def get_all_quizzes(request):
    global _LOADED_QUIZZES

    return jsonify(loadedquizzes=[e.serialize() for e in _LOADED_QUIZZES.values()])


def exists_quiz(id):
    if int(id) > _QUIZNUMBER:
        abort(404)  # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not(id in _LOADED_QUIZZES):
        abort(410)  # error 410: Gone, i.e. it existed but it's not there anymore
