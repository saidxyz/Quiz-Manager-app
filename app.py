import mysql.connector
from flask import Flask, render_template

dbconfig = {'host': 'kark.uit.no',
            'user': 'stud_v23_ssa171',
            'password': 'flaskappquiz23',
            'database': 'stud_v23_ssa171'}
app = Flask(__name__)


@app.route('/')
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
    app.run()
