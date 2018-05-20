from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def f_index():
    return render_template('index.html')
    
@app.route('/LApersonal')
def f_student():
    return render_template("LApersonal.html")
    
@app.route('/index_office')
def f_index_office():
    return render_template("index_office.html")
    
@app.route('/request_tromp')
def f_request():
    return render_template('request_tromp.html')
    
@app.route('/university')
def f_university():
    return render_template('university.html')
    
@app.route('/statistics')
def f_statistics():
    return render_template('statistics.html')
    
@app.route('/ai')
def f_ai():
    return render_template('ai.html')
    
@app.route('/overview')
def f_overview():
    return render_template('overview.html')