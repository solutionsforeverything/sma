from flask import Flask,render_template,request,jsonify,Response,redirect,url_for,session,copy_current_request_context
from flask_socketio import SocketIO,emit,disconnect
import random
from threading import Lock
import aes
import datasourse
import stream

app = Flask(__name__)
async_mode = None
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode, always_connect=True, engineio_logger=True)
list = ['hi', 'ginger', 'demo', 'heaven', 'gear', 'potato', 'crime', 'secret', 'doll', 'magic', 'free', 'hell',
        'positive', 'great', 'glider', 'watermelon', 'gray', 'party', 'women', 'god', 'denver', 'helmet', 'egg',
        'queen', 'king']
thread_lock = Lock()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/login')
def login():
    return render_template('login.html')

def createKey():
    print('Code fr creating key')
    key = 0
    return key


def secretCodeList():
    resList = []
    global list
    s = ""
    for i in range(0,10):
        te = list[random.randint(0, len(list)-1)]
        resList.append(te)
        s+= (te+" ")
    return resList,s


@app.route('/signin-validate' , methods = ['GET','POST'])
def signin_validate():
    if request.method == "POST":
        fullname = request.form['name']
        uname = request.form['uname']
        passw = request.form['up']
        list,str = secretCodeList()


        datasourse.addUserDetails(fullname,uname,passw,str)

        return render_template('secured.html' , user = uname , words = list)


@app.route('/loginValidate' , methods = ['GET' , 'POST'])
def login_validate():
    if request.method == "POST":
        uname = request.form['uname']
        passw = request.form['pass']

        if datasourse.checkLogin(uname,passw) :
            return render_template('entersecure.html' , user = uname)

        return render_template('login.html' , wrong = 1)

@app.route('/<user>/checksecure' , methods = ['GET' , 'POST'])
def check_secure(user):
    if request.method == "POST" :
        temp = datasourse.getSecureWords(user)
        user_word_list = []

        for i in range(1,11):
            user_word_list.append(request.form['w'+str(i)])
        for i in range(0,10) :
            if user_word_list[i] != temp[i] :
                print('enter login')
                return redirect(url_for('login'))

        session['uname'] = user
        return redirect(url_for('inbox' , user = user))


@app.route("/<user>")
def inbox(user) :
    return render_template('inbox.html',user = user)

@app.route('/<user>/compose')
def compose(user):
    return render_template('compose.html' , user = user , success = "0")

@app.route('/<user>/send' , methods = ['GET','POST'])
def send(user):
    print('sending...')
    to = request.form['to']
    msg = request.form['msg']
    fromm = user
    print(user,msg,to)
    enc_msg , nonce , tag =aes.encrypt_AES_GCM(msg,fromm)
    print(enc_msg,nonce,tag)


    # b_id , from , to , e_msg , time , prev_hash

    thread_lock.acquire()
    prev_hash = datasourse.getHashKey()
    datasourse.addData(fromm,to,enc_msg,nonce,tag,prev_hash)
    thread_lock.release()
    return render_template('compose.html' , user = user , success = "1")


@socket_.on('check' , namespace='/test')
def check(message):
    print('checking')
    us = message['user']
    try:
        if session['uname'] != None and us == session['uname']:

            emit('validity', {'status': "ok"})

        else:

            emit('validity', {'status': "notok"})

    except KeyError as e:
        emit('validity', {'status': "notok"})

@socket_.on('get_msg' , namespace='/test')
def getMsg(message):
    user = message['user']
    list = datasourse.getData(user)

    if len(list) == 0 :
        emit('no_msg' , {'no' : '1'})
        return

    sor_list = sorted(list, key=lambda i: i['time'], reverse=True)
    print(sor_list)

    for l in sor_list:
        dec_msg = aes.decrypt_AES_GCM((l['msg'], l['nonce'], l['tag']), l['from'])
        dec_msg = str(dec_msg)
        emit('send_inbox', {'from' : l['from'] , 'time' : l['time'] , 'msg' : dec_msg})


@app.route('/logout')
def logout():
    session.pop('uname')
    return redirect(url_for('home'))


if __name__ == "__main__":
    socket_.run(app,debug=True)
