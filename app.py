from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'preksha-secret-key'  # Required for flashing messages

students = []

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.args.get('query', '')
    filtered_students = [s for s in students if query.lower() in s['name'].lower() or query in s['roll']]

    return render_template('index.html', students=filtered_students, total=len(filtered_students), query=query)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll = request.form['roll']

    if name and roll:
        students.append({'name': name, 'roll': roll})
        flash('Student added successfully!', 'success')
    else:
        flash('Both fields are required!', 'error')

    return redirect(url_for('index'))

@app.route('/delete/<roll>')
def delete_student(roll):
    global students
    students = [s for s in students if s['roll'] != roll]
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/edit/<roll>', methods=['GET', 'POST'])
def edit_student(roll):
    student = next((s for s in students if s['roll'] == roll), None)
    if request.method == 'POST':
        student['name'] = request.form['name']
        student['roll'] = request.form['roll']
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)


if __name__ == "__main__":
    app.run(debug=True)
