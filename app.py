import mysql.connector
from flask import Flask, flash, redirect, render_template, request, session, url_for

dbconfig = {
    "host": "kark.uit.no",
    "user": "stud_v23_ssa171",
    "password": "flaskappquiz23",
    "database": "stud_v23_ssa171",
}

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


@app.route("/home")
def index():
    return render_template("home.html", the_title="Development Quiz App")


@app.route("/", methods=["GET", "POST"])
def login():
    formdata = request.form
    if formdata.get("email") is not None:
        print(formdata.get("email"))
        print(formdata.get("password"))
        conn = dbconnection()
        cursor = conn.cursor()
        
        cursor.execute(
            "select * from users where email=%s and password=%s",
            (formdata.get("email"), formdata.get("password")),
        )
        row = cursor.fetchone()
        print(row)
        if row is not None:
            session["user_id"] = row[0]
            session["is_admin"] = row[5]
            if row[5] == "1":
                return redirect("/admin/quiz")
            else:
                return redirect("/quiz")
        else:
            flash("Error when logging in. Please check email and password", "error")
    return render_template("login.html", the_title="Login")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    print(session.get)
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    formdata = request.form
    if formdata.get("email") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute("select * from users where email=%s", (formdata.get("email"),))
        row = cursor.fetchone()
        if row is not None:
            flash("User already exists.", "error")
        else:
            cursor.execute(
                "insert into users(email,first_name,last_name,password,is_admin) values(%s,%s,%s,%s,%s)",
                (
                    formdata.get("email"),
                    formdata.get("first_name"),
                    formdata.get("last_name"),
                    formdata.get("password"),
                    formdata.get("user_type"),
                ),
            )
            conn.commit()
            flash("User created successfully.", "success")
            return redirect("/")
    return render_template("register.html", the_title="Register")


@app.route("/quiz")
def quiz():
    if checkUserLogin() is None:
        flash("You need to log in first to se Quiz!", "error")
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quiz order by id desc")
    quiz = cursor.fetchall()
    print("quiz")
    for i in quiz:
        print(i)
    cursor = conn.cursor()
    cursor.execute(
        "select * from answer where user_id=%s group by quiz_id",
        (session.get("user_id"),),
    )
    answer = cursor.fetchall()
    print("answer")
    for x in answer:
        print(x)
    answerData = []
    for a in answer:
        if a[4] is not None:
            answerData.append(int(a[4]))
    print("answerData")
    print(answerData)
    for b in answerData:
        print(b)
    return render_template(
        "user/quiz.html", the_title="Quiz", quiz=quiz, answerData=answerData
    )


@app.route("/results")
def results():
    if checkUserLogin() is None:
        flash("You need to log in first to se Results!", "error")
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute(
        "select quiz.* from quiz inner join answer on quiz.id=answer.quiz_id where answer.user_id=%s group by answer.quiz_id order by quiz.id desc",
        (session.get("user_id"),),)
    quiz = cursor.fetchall()
    print("taken quiz")
    for i in quiz:
        print(i)
    return render_template("user/resultslist.html", the_title="Results", quiz=quiz)


@app.route("/admin/quiz")
def admin_quizzes():
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute(
        "select * from quiz where user_id=%s order by id desc",(session.get("user_id"),),)
    result = cursor.fetchall()
    print("result")
    count = 0
    for i in result:
        count += 1
        print(f"{count}: {i}")
    return render_template("admin/manage_quiz.html", the_title="Manage quiz", quiz=result)


@app.route("/admin/create_quiz", methods=["GET", "POST"])
def create_quiz():
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    formdata = request.form
    if formdata.get("title") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute(
            "select * from quiz where quiz_url=%s", (formdata.get("quiz_url"),)
        )
        row = cursor.fetchone()
        if row is not None:
            flash("Quiz URL already exists.", "error")
            # message = "Quiz URL already exists."
        else:
            cursor.execute(
                "insert into quiz(title,quiz_url,user_id) values(%s,%s,%s)",
                (
                    formdata.get("title"),
                    formdata.get("quiz_url"),
                    session.get("user_id"),
                ),
            )
            conn.commit()
            flash("Quiz created successfully.", "success")
            # message = "Quiz created successfully."
            return redirect("/admin/quiz")
    return render_template("admin/create_quiz.html", the_title="Create Quiz")


@app.route("/admin/edit_quiz/<id>", methods=["GET", "POST"])
def edit_quiz(id):
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    formdata = request.form
    if formdata.get("quiz_id") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute(
            "update quiz set title=%s,quiz_url=%s where id=%s and user_id=%s",
            (
                formdata.get("title"),
                formdata.get("quiz_url"),
                id,
                session.get("user_id"),
            ),
        )
        conn.commit()
        flash("Quiz updated successfully.", "info")
        return redirect("/admin/quiz")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute(
        "select * from quiz where id=%s and user_id=%s", (id, session.get("user_id"))
    )
    quizdata = cursor.fetchone()
    print("quizdata")
    for i in quizdata:
        print(i)
    return render_template(
        "admin/edit_quiz.html", the_title="Edit Quiz", quizdata=quizdata
    )


@app.route("/admin/delete_quiz/<id>", methods=["GET", "POST"])
def delete_quiz(id):
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute(
        "delete from quiz where id=%s and user_id=%s", (id, session.get("user_id"))
    )
    conn.commit()
    flash("Quiz deleted successfully.", "warning")
    return redirect("/admin/quiz")


@app.route("/admin/question/<id>/create", methods=["GET", "POST"])
def create_question(id):
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    conn =dbconnection()
    cursor = conn.cursor()
    cursor.execute(
        "select * from quiz where id=%s and user_id=%s", (id, session.get("user_id"))
    )
    quizdata = cursor.fetchone()
    formdata = request.form
    print(quizdata)
    if formdata.get("quiz_id") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute(
            "insert into question(title,option1,option2,option3,option4,answer,quiz_id) values(%s,%s,%s,%s,%s,%s,%s)",
            (
                formdata.get("title"),
                formdata.get("option1"),
                formdata.get("option2"),
                formdata.get("option3"),
                formdata.get("option4"),
                formdata.get("answer"),
                id,
            ),
        )
        conn.commit()
        flash("Question created successfully.", "success")
        return redirect("/admin/question/" + id + "/all")
    return render_template(
        "admin/create_question.html", the_title="Create Question", quizdata=quizdata
    )


@app.route("/admin/question/<id>/all")
def all_question(id):
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute(
        "select * from quiz where id=%s and user_id=%s", (id, session.get("user_id"))
    )
    quizdata = cursor.fetchone()
    cursor = conn.cursor()
    cursor.execute("select * from question where quiz_id=%s order by id desc", (id,))
    quetiondata = cursor.fetchall()
    return render_template(
        "admin/questionall.html",
        the_title="Create Question",
        quizdata=quizdata,
        quetiondata=quetiondata,
    )


@app.route("/admin/edit_question/<id>/<qid>", methods=["GET", "POST"])
def edit_question(id, qid):
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    formdata = request.form
    if formdata.get("quiz_id") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        cursor.execute(
            "update question set title=%s,option1=%s,option2=%s,option3=%s,option4=%s,answer=%s where id=%s and quiz_id=%s",
            (
                formdata.get("title"),
                formdata.get("option1"),
                formdata.get("option2"),
                formdata.get("option3"),
                formdata.get("option4"),
                formdata.get("answer"),
                qid,
                id,
            ),
        )
        conn.commit()
        flash("Question updated successfully.", "info")
        return redirect("/admin/question/" + id + "/all")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from question where id=%s and quiz_id=%s", (qid, id))
    questiondata = cursor.fetchone()
    print(questiondata)
    return render_template(
        "admin/edit_question.html", the_title="Edit Question", questiondata=questiondata
    )


@app.route("/admin/delete_question/<id>/<qid>", methods=["GET", "POST"])
def delete_question(id, qid):
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("delete from question where id=%s and quiz_id=%s", (qid, id))
    conn.commit()
    flash("Question deleted successfully.", "warning")
    return redirect("/admin/question/" + id + "/all")


@app.route("/Manage_quiz")
def quizzes():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """SELECT * FROM quiz"""
    cursor.execute(_SQL)
    result = cursor.fetchall()
    return render_template("admin/manage_quiz.html", the_title="Manage quiz", quiz=result)


@app.route("/admin/all_results")
def all_results():
    if checkUserLogin() is None or checkUserRole("1") is False:
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute(
        "select quiz.*,answer.user_id from quiz inner join answer on quiz.id=answer.quiz_id group by answer.quiz_id order by quiz.id desc"
    )
    quiz = cursor.fetchall()
    # print(quiz)
    return render_template("admin/all_results.html", the_title="All Results", quiz=quiz)


@app.route("/take-quiz/<slug>/question", methods=["GET", "POST"])
def quiz_taken(slug):
    if checkUserLogin() is None:
        return redirect("/")
    formdata = request.form
    retakeQuiz = 0
    if request.args.get("retake") is not None:
        retakeQuiz = 1
    if formdata.get("submitQuiz") is not None:
        conn = dbconnection()
        cursor = conn.cursor()
        print("called")
        if formdata.get("retakeQuiz") == "1":
            print("called 1")
            cursor = conn.cursor()
            cursor.execute(
                "delete from answer where user_id=%s and quiz_id=%s",
                (session.get("user_id"), formdata.get("quiz_id")),
            )
            conn.commit()

        for question in formdata.getlist("questions"):
            print(question)
            marks = 0
            cursor = conn.cursor()
            cursor.execute("select * from question where id=%s", (question,))
            questionData = cursor.fetchone()
            print(questionData)
            print(questionData[6])
            if str(questionData[6]) == str(formdata.get("answer-" + question)):
                marks = 1
            cursor = conn.cursor()
            cursor.execute(
                "insert into answer(question_id,user_id,quiz_id,answer, marks) values(%s,%s,%s,%s,%s)",
                (
                    question,
                    session.get("user_id"),
                    formdata.get("quiz_id"),
                    formdata.get("answer-" + question),
                    marks,
                ),
            )
            conn.commit()

        return redirect("/take-quiz/" + slug + "/result")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quiz where quiz_url=%s", (slug,))
    quizdata = cursor.fetchone()
    print(quizdata)
    cursor = conn.cursor()
    cursor.execute("select * from question where quiz_id=%s", (quizdata[0],))
    questionData = cursor.fetchall()
    return render_template(
        "user/quiz-take.html",
        the_title="Take Quiz",
        quizdata=quizdata,
        questionData=questionData,
        retakeQuiz=retakeQuiz,
    )


@app.route("/take-quiz/<slug>/result")
def quiz_result(slug):
    if checkUserLogin() is None:
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quiz where quiz_url=%s", (slug,))
    quizdata = cursor.fetchone()
    cursor = conn.cursor()
    cursor.execute(
        "select answer.*,question.* from answer inner join question on answer.question_id=question.id  where answer.quiz_id=%s and answer.user_id=%s",
        (quizdata[0], session.get("user_id")),
    )
    answerData = cursor.fetchall()
    # print(answerData)
    cursor = conn.cursor()
    cursor.execute("select * from users where id=%s", (session.get("user_id"),))
    userData = cursor.fetchone()
    totalMarks = 0
    obtainedMarks = 0
    for answer in answerData:
        # print(answer[5])
        totalMarks = totalMarks + 1
        obtainedMarks = obtainedMarks + int(answer[2])
    return render_template(
        "user/results.html",
        the_title="Results",
        answerData=answerData,
        userData=userData,
        quizdata=quizdata,
        totalMarks=totalMarks,
        obtainedMarks=obtainedMarks,
    )


@app.route("/takequiz/<slug>/result/<id>")
def quiz_results(slug, id):
    if checkUserLogin() is None:
        return redirect("/")
    conn = dbconnection()
    cursor = conn.cursor()
    cursor.execute("select * from quiz where quiz_url=%s", (slug,))
    quizdata = cursor.fetchone()
    cursor = conn.cursor()
    cursor.execute(
        "select answer.*,question.* from answer inner join question on answer.question_id=question.id  where answer.quiz_id=%s and answer.user_id=%s",
        (quizdata[0], id),
    )
    answerData = cursor.fetchall()
    # print(answerData)
    cursor = conn.cursor()
    cursor.execute("select * from users where id=%s", (id,))
    userData = cursor.fetchone()
    totalMarks = 0
    obtainedMarks = 0
    for answer in answerData:
        # print(answer[5])
        totalMarks = totalMarks + 1
        obtainedMarks = obtainedMarks + int(answer[2])
    return render_template(
        "user/results.html",
        the_title="Results",
        answerData=answerData,
        userData=userData,
        quizdata=quizdata,
        totalMarks=totalMarks,
        obtainedMarks=obtainedMarks,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
