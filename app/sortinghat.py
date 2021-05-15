import os
from flask import request, Flask, json
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)

@app.route('/sortinghat', methods=['GET', 'POST'])
def sorting_hat():
    if request.method == 'GET':
        return get_sortinghat_question()
    else:
        return get_sortinghat_result()

def get_sortinghat_question():
    filename = 'app/sh_questions.json'
    with open(filename) as questions:
        data = json.load(questions)
        return json.jsonify(data)

def get_sortinghat_result():
    user_answers = request.json
    filename = 'app/sh_results.json'
    score = {
        'Gryffindor': {
            'score': 0,
            'percentage': 0
        },
        'Ravenclaw': {
            'score': 0,
            'percentage': 0
        },
        'Hufflepuff': {
            'score': 0,
            'percentage': 0
        },
        'Slytherin': {
            'score': 0,
            'percentage': 0
        }
    }
    total_points = 0
    with open(filename) as sys_scoring:
        sys_scoring_data = json.load(sys_scoring)
    for answer in user_answers:
        houses = sys_scoring_data[answer['id']][answer['value']]
        for house in houses:
            score[house['id']]['score'] += house['value']
            total_points += house['value']

    app.logger.info("Total points obtained: {}".format(total_points))

    for house_name, house_score in score.items():
        house_score['percentage'] = round(house_score['score'] * 100 / total_points)

    return score

if __name__ == "__main__":
    app.run(host="0.0.0.0")