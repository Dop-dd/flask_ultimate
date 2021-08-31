from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

# for session
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'


#----DATABASE -------------
# connect to DB
def connect_db():
    sql = sqlite3.connect(r'C:\Users\dopdd\Desktop\Flask_apps\data1.db')
    # redern result as dicttionaries
    sql.row_factory = sqlite3.Row 
    return sql

# get the database
def get_db():
    if not hasattr(g, 'sqlite3'):
        #if db not present, add it
        g.sqlite_db = connect_db()
    return g.sqlite_db

# auto close the connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#----End DATABASE -------------

@app.route('/')
def index():
    session.pop('name', None)
    #session['name'] = name 
    return '<h1>hello!</h1>'

@app.route('/home', methods=['GET', 'POST'], defaults={'name' : 'Default'})
@app.route('/home/<name>', methods=['GET', 'POST'])
def home(name):
    session['name'] = name 
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()    
    
    return render_template('home.html', name=name,  display=True, \
         mylist=['one', 'two', 'three', 4], results=results)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession'
    return jsonify({'key': 'value', 'alistkey': [1,2,3,4], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h2>Hi {}. you are from {}. This is the query page </h2>'.format(name, location)

# Refactoring form input to include GET and POST in same route
@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
         return render_template('form.html')        
    else:
        # redirecting to the home page
        name = request.form['name']
        location = request.form['location']

        # send to the db
        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)' ,[name, location])
        db.commit()
        # return '<h1>Hello {}, you are from {}. You have submitted the form successfully!</h1>'.format(name, location)
        return redirect(url_for('home', name=name, location=location))


# json format
@app.route('/processjson', methods=['POST'])
def processjson():
    # get the data
    data = request.get_json()

    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({'result' : 'Success', 'name': name, 'location': location,
                    'randomkeyinlist': randomlist[1]})

# ----Get DATABASE Results---------
@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(results[2]['id'], \
        results[2]['name'], results[2]['location'])

if __name__ == '__main__':
    app.run()