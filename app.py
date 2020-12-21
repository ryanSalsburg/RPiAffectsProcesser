'''
Flask server for CS121 Final Project

Description:
Creates a webpage to record a .wav file from the guitar for any amount of time.
The user can then listen to the 
'''
import random
from flask import Flask, render_template, request, url_for, flash, redirect
import subprocess # add in functionality for record
#Put import for file with distort functions
from distortion import*
from pitch import*
app = Flask(__name__, static_folder='instance/static')
global startRecord
global x
global y

@app.route("/", methods = ['GET', 'POST'])
def start():
    '''Routes user to index page '''
    test2 = 'hidden'
    #return redirect(url_for('login'))
    return render_template('index.html', test2=test2, x = 'null')

@app.route('/record' , methods = ['POST'])
def record():
    #Run record command
    global x
    x = random.randint(1,10000)
    x = str(x) +'.wav'
    global startRecord
    startRecord = subprocess.Popen("exec arecord -D plughw:1,0 -f cd "+x, stdout=subprocess.PIPE, shell=True)
    #may need to move input to different
    test1 = 'hidden'
    return render_template('index.html', test1=test1, x=x)

@app.route('/end' , methods = ['POST', 'GET'])
def end():
    #Run stop record command
    try:
        global startRecord
        global x
        startRecord.kill()
        #may need to move input to different
        #try:
            #subprocess.run("rm instance/static/input.wav", shell=True, check=True)
        #except:
            #print("fail")
        subprocess.run("mv "+ x +" instance/static", shell=True, check=True)
        test2 = 'hidden'
    except:
        print("fail")
    return render_template('index.html', test2 = test2, x = x)

@app.route('/effect1' , methods = ['GET', 'POST'])
def effectOne():
    #Run effect 1
    global x
    global y
    y = random.randint(1,10000)
    y = str(y)+".wav"
    distortion(x,y)
    return render_template('index.html', out = y, x=x, test2 = 'hidden')

@app.route('/effect2' , methods = ['GET', 'POST'])
def effectTwo():
    #Run effect 2
    global x
    global y
    y = random.randint(1,10000)
    y = str(y)+".wav"
    boost(x,y)
    return render_template('index.html',out = y, x=x, test2 = 'hidden')

@app.route('/effect3' , methods = ['GET', 'POST'])
def effectThree():
    #Run effect 3
    global x
    global y
    y = random.randint(1,10000)
    y = str(y)+".wav"
    tremelo(x,y)
    return render_template('index.html',out = y, x=x,test2 = 'hidden')

@app.route('/effect4' , methods = ['GET', 'POST'])
def effectFour():
    #Run effect 4
    global x
    global y
    y = random.randint(1,10000)
    y = str(y)+".wav"
    pitch(x, y)
    return render_template('index.html',out = y, x=x,test2 = 'hidden')


'''
@app.route('/effect5' , methods = ['GET', 'POST'])
def effectFive():
    #Run effect 5
    effect5()
    return render_template('index.html')
'''
