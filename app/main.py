from flask import Blueprint, render_template, request, redirect, url_for,jsonify

main = Blueprint("main", __name__, url_prefix="/api/v1/bookmarks")


@main.route('/home')
def home():
    inp = request.form.get('SOME_INPUT')
    todo_item = request.form.get('add-todo')
    print(request.args)
    print(todo_item)
    print(inp)
    return render_template('home.html', sample_variable="XXXXXXXXXXXXXXX")


@main.post('/handle_data')
def handle_data():
    projectpath = request.form['projectFilepath']
    print(projectpath)
    return jsonify({'x': 'y'})


@main.post('/add_todo')
def add_todo():
    # todo_item = request.form['add-todo']
    email = request.form['register-email']
    password = request.form['input-password']
    print(email)
    print(password)
    return jsonify({'s': 'x'})
