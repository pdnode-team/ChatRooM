#api server service
import sys
from flask import *
from fs.osfs import *
Mf :OSFS =None
Users=None
app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return jsonify({"message":"Chatroom.\nhttps://github.com/pdnode-team/ChatRooM"})

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if not('username' in request.form and 'password' in request.form):
            return "Login failed:Invalid.",417
        username=request.form['username'],pwd=request.form['password']
        if not username in Users:
            return "Login failed:invalid username.",403
        Uinf=json.loads(Mf.readtext(f"./data/User/{username}/.register",encoding="utf-8"))
        if pwd!=Uinf['password']:
            return "Login failed:invalid password.",403
        Upr=json.loads(Mf.readtext(f"./data/User/{username}/.prconfig",encoding="utf-8"))
        if Upr['login']==0:
            return "Login failed: Banned",403
        session['User']={"Name":username,"PR":Upr,"reg":Uinf}
        return "[Login] Succeed.",200
    return "",500

@app.route('/register',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if not('username' in request.form and 'password' in request.form):
            return "Register failed:Invalid.",417
        username=request.form['username'],pwd=request.form['password']
        ###
    return "",500

def run(Mf : OSFS):
    C=json.loads(Mf.readtext("./.Sconfig"))
    globals["Mf"]=Mf
    Users=json.loads(Mf.readtext("./data/User/.inf"))
    app.run(debug=False,host=C['ip'],port=C['port'])

if __name__=="__main__": #测试使用
    app.run(debug=False,host='127.0.0.1',port=44444)