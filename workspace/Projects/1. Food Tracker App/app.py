from flask import Flask, render_template

app = Flask(__name__)

# home
@app.route('/')
def index():
    return render_template('home.html')

# view
@app.route('/view')
def view():
    return render_template('day.html')

#add food
@app.route('/food')
def food():
    return render_template('add_food.html')





if __name__ == '__main__':
    app.run(debug=True)