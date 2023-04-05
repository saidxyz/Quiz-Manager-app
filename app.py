import mysql.connector
from flask import Flask, render_template, url_for

dbconfig = {'host': 'kark.uit.no',
            'user': 'stud_v23_ssa171',
            'password': 'flaskappquiz23',
            'database': 'stud_v23_ssa171'}
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html', the_title='Development page')


@app.route('/login')
def login():
    return render_template('login.html', the_title='Login')


@app.route('/register')
def register():
    return render_template('register.html', the_title='Register')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html', the_title='Quiz')


@app.route('/results')
def results():
    return render_template('bruker/results.html', the_title='Results')


@app.route('/create_quiz')
def create_quiz():
    return render_template('admin/create_quiz.html', the_title='Create Quiz')


@app.route('/create_question')
def create_question():
    return render_template('admin/create_question.html', the_title='Create Question')


@app.route('/question')
def question():
    return render_template('bruker/question.html', the_title='Question')


@app.route('/quizzes')
def quizzes():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """SELECT * FROM quiz"""
    cursor.execute(_SQL)
    result = cursor.fetchall()
    return render_template('admin/quizzes.html', the_title='Quizzes', quiz=result)


@app.route('/all_results')
def all_results():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """SELECT * FROM results"""
    cursor.execute(_SQL)
    result = cursor.fetchall()
    return render_template('admin/all_results.html', the_title='All Results', results=result)


@app.route('/index')
def hello() -> 'html':
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """SELECT id, givenName, lastName, email, studyProgram FROM student"""
    cursor.execute(_SQL)
    result = cursor.fetchall()
    return render_template('students.html',
                           students=result)
    cursor.close()
    conn.close()


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)


if __name__ == '__main__':
    app.run(debug=True)
