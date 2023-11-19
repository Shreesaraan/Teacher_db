import json
import pymongo
from bson import ObjectId

MONGO_CONNECTION_STRING = "mongodb+srv://Shreedev2k3:ShikaLoki@cluster0.dl01wdh.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "teacher_management"
TEACHERS_COLLECTION_NAME = "teachers"

client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[DB_NAME]
teachers_collection = db[TEACHERS_COLLECTION_NAME]

def load_teachers():
    teachers = teachers_collection.find()
    return list(teachers)

def save_teachers(teachers):
    teachers_collection.insert_many(teachers)

def show_all_teachers():
    teachers = load_teachers()
    for teacher in teachers:
        print_teacher_info(teacher)

def add_teacher():
    full_name = input("Enter teacher's full name: ")
    age = int(input("Enter teacher's age: "))
    dob = input("Enter teacher's date of birth (YYYY-MM-DD): ")
    num_classes = int(input("Enter the number of classes the teacher teaches: "))

    teacher = {
        'full_name': full_name,
        'age': age,
        'dob': dob,
        'num_classes': num_classes
    }

    try:
        teachers_collection.insert_one(teacher)
        print("Teacher added successfully.")
    except pymongo.errors.DuplicateKeyError:
        print("Error: Duplicate key. The teacher ID is not unique.")
    except Exception as e:
        print(f"An error occurred: {e}")

def filter_teachers_by_age():
    age = int(input("Enter age to filter teachers: "))
    teachers = [teacher for teacher in load_teachers() if teacher['age'] == age]
    for teacher in teachers:
        print_teacher_info(teacher)

def filter_teachers_by_num_classes():
    num_classes = int(input("Enter the number of classes to filter teachers: "))
    teachers = [teacher for teacher in load_teachers() if teacher['num_classes'] == num_classes]
    for teacher in teachers:
        print_teacher_info(teacher)

def search_teacher():
    full_name = input("Enter the full name of the teacher to search: ")
    matching_teachers = [teacher for teacher in load_teachers() if teacher['full_name'].lower() == full_name.lower()]

    if matching_teachers:
        for teacher in matching_teachers:
            print_teacher_info(teacher)
    else:
        print("Teacher not found.")

def update_teacher():
    teacher_name = input("Enter the teacher's full name to update: ")
    existing_teacher = teachers_collection.find_one({'full_name': {'$regex': f'^{teacher_name}$', '$options': 'i'}})

    if existing_teacher:
        new_num_classes = int(input("Enter the new number of classes: "))
        teachers_collection.update_one({'_id': existing_teacher['_id']}, {'$set': {'num_classes': new_num_classes}})
        print("Teacher updated successfully.")
    else:
        print("Teacher not found. Enter a valid name.")

def delete_teacher():
    teacher_name = input("Enter the teacher's full name to delete: ")
    existing_teacher = teachers_collection.find_one({'full_name': {'$regex': f'^{teacher_name}$', '$options': 'i'}})

    if existing_teacher:
        result = teachers_collection.delete_one({'_id': existing_teacher['_id']})
        if result.deleted_count > 0:
            print("Teacher deleted successfully.")
        else:
            print("An error occurred while deleting the teacher.")
    else:
        print("Teacher not found. Enter a valid name.")

def calculate_average_classes():
    teachers = load_teachers()
    total_classes = sum(teacher['num_classes'] for teacher in teachers)
    total_teachers = len(teachers)
    
    if total_teachers > 0:
        average_classes = total_classes / total_teachers
        print(f"The average number of classes taken by teachers is: {average_classes}")
    else:
        print("No teachers found.")

def print_teacher_info(teacher):
    print(f"Teacher ID: {teacher['_id']}")
    print(f"Full Name: {teacher['full_name']}")
    print(f"Age: {teacher['age']}")
    print(f"Date of Birth: {teacher['dob']}")
    print(f"Number of Classes: {teacher['num_classes']}")
    print("\n")

def main():
    while True:
        print("\nTeacher Management Application")
        print("1. Show all teachers.")
        print("2. Add a teacher.")
        print("3. Filter teachers by age.")
        print("4. Filter teachers by the number of classes.")
        print("5. Search for a teacher.")
        print("6. Update a teacher's record.")
        print("7. Delete a teacher.")
        print("8. Calculate average number of classes.")
        print("9. Quit.")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            show_all_teachers()
        elif choice == '2':
            add_teacher()
        elif choice == '3':
            filter_teachers_by_age()
        elif choice == '4':
            filter_teachers_by_num_classes()
        elif choice == '5':
            search_teacher()
        elif choice == '6':
            update_teacher()
        elif choice == '7':
            delete_teacher()
        elif choice == '8':
            calculate_average_classes()
        elif choice == '9':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
