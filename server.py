from flask import Flask, render_template, request, redirect, session, Markup, flash
import random, datetime
from datetime import datetime, time, date
app = Flask(__name__)
app.secret_key = "123456789"

@app.route('/')
def index():
    if 'yourGold' not in session and 'newGold' not in session:
        session['yourGold'] = 0
        session['newGold'] = 0
    return render_template('index.html')

@app.route('/process_money', methods = ['POST'])
def farm():
    time = datetime.now()
    now = time.strftime("%B %d, %Y %H:%M:%S")
    if 'activityLog' not in session:
        session['activityLog'] = []
    if request.form['location'] == "farm":
        session['newGold'] = random.randint(10,20)
        session['activityLog'].insert(0, "<p style='color:green;'>You visited the farm and collected " + str(session['newGold']) + " gold. (" + now + ")</p>")
    if request.form['location'] == "cave":
        session['newGold'] = random.randint(5,10)
        session['activityLog'].insert(0, "<p style='color:green;'>You visited the cave and collected " + str(session['newGold']) + " gold. (" + now + ")</p>")
    if request.form['location'] == "house":
        session['newGold'] = random.randint(2,5)
        session['activityLog'].insert(0, "<p style='color:green;'>You visited the house and collected " + str(session['newGold']) + " gold. (" + now + ")</p>")
    if request.form['location'] == "casino":
        if session['yourGold'] < 50:
            session['activityLog'].insert(0, "<p>You're too poor to gamble. (" + now + ")</p>")
            session['newGold'] = 0
        else:
            session['newGold'] = random.randint(-50,50)
            if session['newGold'] == 0:
                session['activityLog'].insert(0, "<p style='color:green;'>You visited the casino and broke even. (" + now + ")</p>")
            elif session['newGold'] > 0:
                session['activityLog'].insert(0, "<p style='color:green;'>You visited the casino and won " + str(session['newGold']) + " gold. (" + now + ")</p>")
            elif session['newGold'] < 0:
                session['activityLog'].insert(0, "<p style='color:red;'>You visited the casino and lost " + str(-session['newGold']) + " gold. (" + now + ")</p>")
    session['yourGold'] += session['newGold']
    if request.form['location'] == "start_over":
        session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True) 