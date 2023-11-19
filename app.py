from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson import ObjectId
from flask import request

app = Flask(__name__)

MONGO_CONNECTION_STRING = "mongodb+srv://Shreedev2k3:ShikaLoki@cluster0.dl01wdh.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "teacher_management"
TEACHERS_COLLECTION_NAME = "teachers"

client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[DB_NAME]
teachers_collection = db[TEACHERS_COLLECTION_NAME]

def load_teachers():
    teachers = teachers_collection.find()
    return list(teachers)

def save_teacher(teacher):
    teachers_collection.insert_one(teacher)


def search_teacher_logic(full_name):
    return [teacher for teacher in load_teachers() if teacher['full_name'].lower() == full_name.lower()]

def filter_teachers_by_age_logic(age):
    return [teacher for teacher in load_teachers() if teacher['age'] == age]

def filter_teachers_by_classes_logic(operator, num_classes):
    teachers = load_teachers()

    if operator == 'greater':
        return [teacher for teacher in teachers if teacher['num_classes'] > num_classes]
    elif operator == 'less':
        return [teacher for teacher in teachers if teacher['num_classes'] < num_classes]
    elif operator == 'equal':
        return [teacher for teacher in teachers if teacher['num_classes'] == num_classes]
    else:
        return None 


def delete_teacher_by_name(full_name):
    result = teachers_collection.delete_one({'full_name': full_name})
    return result.deleted_count > 0


def update_teacher_by_name(full_name, new_num_classes):
    teachers_collection.update_one({'full_name': full_name}, {'$set': {'num_classes': new_num_classes}})

def calculate_average_num_classes():
    teachers = load_teachers()

    if not teachers:
        return None 

    total_classes = sum(teacher['num_classes'] for teacher in teachers)
    average_classes = total_classes / len(teachers)
    
    return average_classes


@app.route('/')
def index():
    teachers = load_teachers()
    average_classes = None
    if teachers:
        total_classes = sum(teacher['num_classes'] for teacher in teachers)
        average_classes = total_classes / len(teachers)

    return render_template('index.html', teachers=teachers, average_classes=average_classes)

    return render_template('index.html')

@app.route('/show_all_teachers')
def show_all_teachers():
    teachers = load_teachers()
    return render_template('show_all_teachers.html', teachers=teachers)

@app.route('/add_teachers', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = int(request.form['age'])
        dob = request.form['dob']
        num_classes = int(request.form['num_classes'])

        teacher = {
            'full_name': full_name,
            'age': age,
            'dob': dob,
            'num_classes': num_classes
        }

        save_teacher(teacher)
        return redirect(url_for('show_all_teachers'))

    return render_template('add_teachers.html')

@app.route('/filter_teachers_by_age', methods=['GET', 'POST'])
def filter_teachers_by_age_route():
    if request.method == 'POST':
        age = int(request.form['age'])
        teachers = filter_teachers_by_age_logic(age)
        return render_template('filtered_teachers.html', teachers=teachers, filter_type='Age', filter_value=age)

    return render_template('filter_teachers_by_age.html')

@app.route('/filter_teachers_by_classes', methods=['GET', 'POST'])
def filter_teachers_by_classes_route():
    if request.method == 'POST':
        operator = request.form['operator']
        num_classes = int(request.form['num_classes'])
        filtered_teachers = filter_teachers_by_classes_logic(operator, num_classes)
        if not filtered_teachers:
            message = f"No teachers with number of classes {operator} than {num_classes} found."
        else:
            message = None
        return render_template('filtered_teachers.html', teachers=filtered_teachers, filter_type='Number of Classes', filter_value=num_classes, message=message)
    return render_template('filter_teachers_by_classes.html')


@app.route('/search_teacher', methods=['GET', 'POST'])
def search_teacher_route():
    if request.method == 'POST':
        full_name = request.form['full_name']
        teachers = search_teacher_logic(full_name)
        return render_template('filtered_teachers.html', teachers=teachers, filter_type='Full Name', filter_value=full_name)
    return render_template('search_teacher.html')


@app.route('/update_teacher', methods=['GET', 'POST'])
def update_teacher_route():
    if request.method == 'POST':
        full_name = request.form['full_name']
        new_num_classes = int(request.form['new_num_classes'])
        if search_teacher_logic(full_name):
            update_teacher_by_name(full_name, new_num_classes)
            return redirect(url_for('show_all_teachers'))
        else:
            return render_template('teacher_not_found.html')

    return render_template('update_teacher.html')


@app.route('/delete_teacher', methods=['GET', 'POST'])
def delete_teacher_route():
    if request.method == 'POST':
        full_name = request.form['full_name']
        if delete_teacher_by_name(full_name):
            return redirect(url_for('show_all_teachers'))
        else:
            return render_template('teacher_not_found.html')

    return render_template('delete_teacher.html')


if __name__ == '__main__':
    app.run(debug=True)
