import mysql.connector
from flask import Flask, redirect, render_template, request, session, url_for

dbconfig = {'host': 'kark.uit.no',
            'user': 'stud_v23_ssa171',
            'password': 'flaskappquiz23',
            'database': 'stud_v23_ssa171'}
app = Flask(__name__)
app.config["SECRET_KEY"] = "$5123F324"


def dbconnection():
    conn = mysql.connector.connect(**dbconfig)

    return conn


def checkUserLogin():
    if session.get("user_id") is not None:
        return session.get("user_id")
    else:
        return None


def checkUserRole(role):
    if session.get("is_admin") == role:
        return True
    else:
        return False


@app.route('/')
def index():
    return render_template('home.html', the_title='Development page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    formdata = request.form
    if (formdata.get("email") is not None):
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("select * from users where email=%s and password=%s",
                       (formdata.get("email"), formdata.get("password")))
        row = cursor.fetchone()
        print(row)
        if row is not None:
            session["user_id"] = row[0]
            session["is_admin"] = row[5]
            if row[5] == '1':
                return redirect("/admin/quiz")
            else:
                return redirect("/quiz")
        else:
            message = "Invalid login credentials."
    return render_template('login.html', the_title='Login', message=message)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")


@app.route('/register', methods=["GET", "POST"])
def register():
    message = ""
    formdata = request.form
    if (formdata.get("email") is not None):
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("select * from users where email=%s",
                       (formdata.get("email"),))
        row = cursor.fetchone()
        if row is not None:
            message = "User already exists."
        else:
            cursor.execute(
                "insert into users(email,first_name,last_name,password,is_admin) values(%s,%s,%s,%s,%s)", (formdata.get("email"), formdata.get("first_name"), formdata.get("last_name"), formdata.get("password"), formdata.get("user_type")))
            conn.commit()
            message = "User created successfully."
            return redirect("/login")
    return render_template('register.html', the_title='Register', message=message)


@app.route('/categories')
def categories():
    if checkUserLogin() is None:
        return redirect("/login")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quizz order by id desc")
    quiz = cursor.fetchall()
    return render_template('categories.html', the_title='Categories', quiz=quiz)


@app.route('/quiz')
def quiz():
    if checkUserLogin() is None:
        return redirect("/login")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quizz order by id desc")
    quiz = cursor.fetchall()
    return render_template('user/quiz.html', the_title='Quiz', quiz=quiz)


@app.route('/results')
def results():
    return render_template('bruker/results.html', the_title='Results')


@app.route('/admin/quiz')
def admin_quizzes():
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quizz where user_id=%s order by id desc",
                   (session.get("user_id"),))
    result = cursor.fetchall()
    return render_template('admin/quizzes.html', the_title='Quizzes', quiz=result)



@app.route('/admin/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    message = ""
    formdata = request.form
    if (formdata.get("title") is not None):
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("select * from quizz where quiz_url=%s",
                       (formdata.get("quiz_url"),))
        row = cursor.fetchone()
        if row is not None:
            message = "Quiz URL already exists."
        else:
            cursor.execute(
                "insert into quizz(title,quiz_url,user_id) values(%s,%s,%s)", (formdata.get("title"), formdata.get("quiz_url"), session.get("user_id")))
            conn.commit()
            message = "Quiz created successfully."
            return redirect("/admin/quiz")
    return render_template('admin/create_quiz.html', the_title='Create Quiz', message=message)


@app.route('/admin/edit_quiz/<id>', methods=['GET', 'POST'])
def edit_quiz(id):
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    formdata = request.form
    if formdata.get("quiz_id") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("update quizz set title=%s,quiz_url=%s where id=%s and user_id=%s",
                       (formdata.get("title"), formdata.get("quiz_url"), id, session.get('user_id')))
        conn.commit()
        return redirect("/admin/quiz")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quizz where id=%s and user_id=%s",
                   (id, session.get('user_id')))
    quizdata = cursor.fetchone()
    return render_template('admin/edit_quiz.html', the_title='Edit Quiz', quizdata=quizdata)


@app.route('/admin/delete_quiz/<id>', methods=['GET', 'POST'])
def delete_quiz(id):
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("delete from quizz where id=%s and user_id=%s",
                   (id, session.get('user_id')))
    conn.commit()
    return redirect("/admin/quiz")


@app.route('/admin/question/<id>/create', methods=['GET', 'POST'])
def create_question(id):
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quizz where id=%s and user_id=%s",
                   (id, session.get('user_id')))
    quizdata = cursor.fetchone()
    formdata = request.form
    if formdata.get("quiz_id") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("insert into question(title,option1,option2,option3,option4,answer,quiz_id) values(%s,%s,%s,%s,%s,%s,%s)",
                       (formdata.get("title"), formdata.get("option1"), formdata.get("option2"), formdata.get("option3"), formdata.get("option4"), formdata.get("answer"), id))
        conn.commit()
        return redirect("/admin/question/"+id+"/all")
    return render_template('admin/create_question.html', the_title='Create Question', quizdata=quizdata)


@app.route('/admin/question/<id>/all')
def all_question(id):
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quizz where id=%s and user_id=%s",
                   (id, session.get('user_id')))
    quizdata = cursor.fetchone()
    formdata = request.form
    cursor = conn.cursor()
    cursor.execute(
        "select * from question where quiz_id=%s order by id desc", (id,))
    quetiondata = cursor.fetchall()
    return render_template('admin/questionall.html', the_title='Create Question', quizdata=quizdata, quetiondata=quetiondata)


@app.route('/admin/edit_question/<id>/<qid>', methods=['GET', 'POST'])
def edit_question(id, qid):
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    formdata = request.form
    if formdata.get("quiz_id") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("update question set title=%s,option1=%s,option2=%s,option3=%s,option4=%s,answer=%s where id=%s and quiz_id=%s",
                       (formdata.get("title"), formdata.get("option1"), formdata.get("option2"), formdata.get("option3"), formdata.get("option4"), formdata.get("answer"), qid, id))
        conn.commit()
        return redirect("/admin/question/"+id+"/all")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from question where id=%s and quiz_id=%s",
                   (qid, id))
    questiondata = cursor.fetchone()
    return render_template('admin/edit_question.html', the_title='Edit Question', questiondata=questiondata)


@app.route('/admin/delete_question/<id>/<qid>', methods=['GET', 'POST'])
def delete_question(id, qid):
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("delete from question where id=%s and quiz_id=%s",
                   (qid, id))
    conn.commit()
    return redirect("/admin/question/"+id+"/all")


@app.route('/question')
def question():
    return render_template('bruker/question.html', the_title='Question')


@app.route('/quizzes')
def quizzes():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """SELECT * FROM quizz"""
    cursor.execute(_SQL)
    result = cursor.fetchall()
    return render_template('admin/quizzes.html', the_title='Quizzes', quiz=result)


@app.route('/all_results')
def all_results():
    if checkUserLogin() is None or checkUserRole('1') is False:
        return redirect("/login")
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """SELECT * FROM results"""
    cursor.execute(_SQL)
    result = cursor.fetchall()
    return render_template('admin/all_results.html', the_title='All Results', results=result)


@app.route('/take-quiz/<slug>/question', methods=['GET', 'POST'])
def quiz_taken(slug):
    if checkUserLogin() is None:
        return redirect("/login")
    formdata = request.form
    if formdata.get('submitQuiz') is not None:
        conn = dbconnection()
        return redirect("/take-quiz/"+slug+"/result")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quizz where quiz_url=%s", (slug,))
    quizdata = cursor.fetchone()
    cursor = conn.cursor()
    cursor.execute("select * from question where quiz_id=%s", (quizdata[0],))
    questionData = cursor.fetchall()
    return render_template('user/quiz-take.html', the_title='Take Quiz', quizdata=quizdata, questionData=questionData)


@app.route('/take-quiz/<slug>/result')
def quiz_result(slug):
    return "success"


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
