from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template("index.html", students=students)


@app.route('/add', methods=['GET','POST'])
def add():

    if request.method == 'POST':

        name = request.form['name']
        course = request.form['course']
        email = request.form['email']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO students(name,course,email) VALUES (?,?,?)",
                     (name,course,email))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template("add.html")


@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    if request.method == 'POST':

        name = request.form['name']
        course = request.form['course']
        email = request.form['email']

        conn.execute(
        "UPDATE students SET name=?,course=?,email=? WHERE id=?",
        (name,course,email,id))

        conn.commit()
        conn.close()

        return redirect('/')

    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()

    return render_template("edit.html", student=student)


@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')


app.run(debug=True)
