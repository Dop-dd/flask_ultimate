from flask import Flask, jsonify, request, url_for, redirect, session

app = Flask(__name__)

# for session
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret!'

@app.route('/')
def index():
    return '<h1>hello!</h1>'

@app.route('/home', methods=['GET', 'POST'], defaults={'name' : 'Default'})
@app.route('/home/<name>', methods=['GET', 'POST'])
def home(name):
    session.pop('name', None)
    #session['name'] = name 
    return '<h2> hi {} you are on the home page </h2>'.format(name)

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
        return '''<form method="POST" action="/theform">
                    <input type="text" name="name">
                    <input type="text" name="location">
                    <input type="submit" value="Submit">
                </form>'''
    else:
        # redirecting to the home page
        name = request.form['name']
        location = request.form['location']
        # return '<h1>Hello {}, you are from {}. You have submitted the form successfully!</h1>'.format(name, location)
        return redirect(url_for('home', name=name, location=location))

# form data ha
# @app.route('/process', methods=['POST'])
# def process():
#     name = request.form['name']
#     location = request.form['location']

#     return '<h1>Hello {}, you are from {}. You have submitted the form successfully!</h1>'.format(name, location)

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

if __name__ == '__main__':
    app.run()