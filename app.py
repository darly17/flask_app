from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import os
from models.system import System
from models.course_project import Course_project
import json
from datetime import datetime
from models.student import Student
from pathlib import Path

DATA_DIR = Path("data_bases")
SUBMITTED_PROJECTS_FILE = DATA_DIR / "submitted_projects.json"
KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"
QUESTIONS_FILE = DATA_DIR / "questions.json"
THEME_FILE = DATA_DIR / "theme.json"
INFO_FILE = DATA_DIR / "info.json"
SYSTEM_STATE_FILE = DATA_DIR / "system_state.pkl"

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'



def save_system(system):
    with open(SYSTEM_STATE_FILE, 'wb') as f:
        pickle.dump(system, f)

def get_system():
    if not SYSTEM_STATE_FILE.exists():
        return System()
    with open(SYSTEM_STATE_FILE, 'rb') as f:
        return pickle.load(f)
    



def save_submitted_project(student_info, project_info):
    
    if not SUBMITTED_PROJECTS_FILE.exists():
        SUBMITTED_PROJECTS_FILE.write_text("[]")
    try:
        with open(SUBMITTED_PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        projects = []
    
    project_data = {
        'student': student_info,
        'project': project_info,
        'submission_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    projects.append(project_data)
    
    with open(SUBMITTED_PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

@app.route('/submitted_projects')
def submitted_projects():
    
    try:
        with open(SUBMITTED_PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        projects = []
    
    return render_template('submitted_projects.html', projects=projects)

@app.route('/pass_project')
def pass_project():
    system = get_system()
    result = system._student.pass_corse_project(system._professor, system._course_project)
    
    if result:
       
        student_info = {
            'name': system._student._name,
            'group': system._student._group,
            'number': system._student._student_number
        }
        
        project_info = {
            'theme': system._course_project._theme,
            'text': system._course_project._text,
            'work_plan': system._course_project._work_plan
        }
        
        save_submitted_project(student_info, project_info)
        
        
        system._course_project = Course_project(["12.02","13.03","14.04"])
        save_system(system)
    
    return render_template('pass_project.html', passed=result)

@app.route('/')
def index():
    system = get_system()
    student = system._student
    return render_template('index.html', 
                         student_name=student._name,
                         student_age=student._age,
                         student_group=student._group,
                         student_number=student._student_number)

@app.route('/change_student', methods=['GET', 'POST'])
def change_student():
    system = get_system()
    if request.method == 'POST':
        try:
            name = request.form['name']
            age = int(request.form['age'])
            group = request.form['group']
            number = request.form['number']
            
            if number not in "1234567":
                flash("Number must be between 1 and 7", "error")
                return redirect(url_for('change_student'))
            
            
            system._student = Student(name, age, group, number)
            save_system(system)
            flash("Student information updated successfully", "success")
            return redirect(url_for('index'))
        except ValueError:
            flash("Please enter valid data", "error")
            return redirect(url_for('change_student'))
    
    return render_template('change_student.html')

@app.route('/choose_theme')
def choose_theme():
    system = get_system()
    system._student.choose_theme(system._course_project)
    save_system(system)
    return render_template('choose_theme.html', theme=system._course_project._theme)

@app.route('/work_plan', methods=['GET', 'POST'])
def work_plan():
    system = get_system()
    if request.method == 'POST':
        item_number = request.form['item_number']
        subtask = request.form['subtask']
        
        if not item_number.strip() or not subtask.strip():
            flash("Please enter both item number and text", "error")
        else:
            system._student.edit_plan(system._course_project, item_number, subtask)
            save_system(system)
            flash("Work plan updated successfully", "success")
    
    return render_template('work_plan.html', work_plan=system._course_project._work_plan)

@app.route('/analyze_info')
def analyze_info():
    system = get_system()
    try:
        system._student.get_information()
        system._student.analyse_information(system._course_project)
        save_system(system)
        return render_template('analyze_info.html', 
                             analyzed_info=system._student._analysed_info_for_cp,
                             theme=system._course_project._theme)
    except UnboundLocalError:
        flash("Please choose a theme first", "error")
        return redirect(url_for('index'))

@app.route('/write_text')
def write_text():
    system = get_system()
    try:
        system._student.write_text(system._course_project)
        save_system(system)
        return render_template('write_text.html', text=system._course_project._text)
    except UnboundLocalError:
        flash("Please choose a theme and analyze information first", "error")
        return redirect(url_for('index'))

@app.route('/edit_text', methods=['GET', 'POST'])
def edit_text():
    system = get_system()
    if request.method == 'POST':
        str_to_remove = request.form['str_to_remove']
        try:
            system._student.edit_text(system._course_project, str_to_remove)
            save_system(system)
            flash("Text edited successfully", "success")
        except BaseException:
            flash("Please complete previous steps first", "error")
    
    return render_template('edit_text.html', text=system._course_project._text)

@app.route('/consultation')
def consultation():
    system = get_system()
    system._student.consultation_with_professor(system._professor, system._research)
    save_system(system)
    return render_template('consultation.html', answers=system._research._answers)



if __name__ == '__main__':
    app.run(debug=True)