from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'practice_matrix.db')

@app.route('/')
def index():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM practice_matrix")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        compname = request.form['compname']
        contacts = request.form['contacts']
        direction = request.form['direction']
        people = request.form['people']
        comment = request.form['comment']
        ifcontract = request.form['ifcontract']
        direction_code = request.form['direction_code']
        ownership_form = request.form['ownership_form']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO practice_matrix (compname, contacts, direction, people, comment, ifcontract, direction_code, ownership_form) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (compname, contacts, direction, people, comment, ifcontract, direction_code, ownership_form))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route('/edit/<string:name>', methods=['GET', 'POST'])
def edit(name):
    if request.method == 'POST':
        new_compname = request.form['compname']
        new_contacts = request.form['contacts']
        new_direction = request.form['direction']
        new_people = request.form['people']
        new_comment = request.form['comment']
        new_ifcontract = request.form['ifcontract']
        new_direction_code = request.form['direction_code']
        new_ownership_form = request.form['ownership_form']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE practice_matrix SET compname = ?, contacts = ?, direction = ?, people = ?, comment = ?, ifcontract = ?, direction_code = ?, ownership_form = ? WHERE compname = ?",
                       (new_compname, new_contacts, new_direction, new_people, new_comment, new_ifcontract, new_direction_code, new_ownership_form, name))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM practice_matrix WHERE compname = ?", (name,))
        data = cursor.fetchone()
        conn.close()
        return render_template('edit.html', data=data)

@app.route('/delete/<string:name>')
def delete(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM practice_matrix WHERE compname = ?", (name,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
