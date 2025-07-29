#api server service
import sys
from flask import *
from fs.osfs import *
from colorama import *

def Reg(Mf:OSFS,RegInf:dict):
    Mf.makedir(f"./data/User/{RegInf['Name']}")
    List=json.loads(Mf.readtext("./data/User/.inf",encoding="utf-8"))
    List.append(RegInf['Name'])
    Mf.writetext("./data/User/.inf",json.dumps(List,ensure_ascii=False))
    Mf.writetext(f"./data/User/{RegInf['Name']}/.register",json.dumps(RegInf,ensure_ascii=False))
    Mf.writetext(f"./data/User/{RegInf['Name']}/.prconfig",json.dumps({"login":1,},ensure_ascii=False))
    Mf.writetext(f"./data/User/{RegInf['Name']}/.group",json.dumps({},ensure_ascii=False))

init(autoreset=True)
Mf :OSFS =None
Cback=None
Sfg : dict=None
Users=None
app=Flask(__name__)

@app.before_request
def before_request():
    global Mf, Cback, Sfg, Users
    Users=json.loads(Mf.readtext("./data/User/.inf"))

@app.route('/',methods=['GET'])
def home():
    return jsonify({"message":"Chatroom.\nhttps://github.com/pdnode-team/ChatRooM"})

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if not('username' in request.form and 'password' in request.form):
            return jsonify({"message":"Login failed:Invalid."}),417
        username=request.form['username'],pwd=request.form['password']
        if not username in Users:
            return jsonify({"message":"Login failed:invalid username or password."}),403
        Uinf=json.loads(Mf.readtext(f"./data/User/{username}/.register",encoding="utf-8"))
        if pwd!=Uinf['password']:
            return jsonify({"message":"Login failed:invalid username or password."}),403
        Upr=json.loads(Mf.readtext(f"./data/User/{username}/.prconfig",encoding="utf-8"))
        if Upr['login']==0:
            return jsonify({"message":"Login failed: Banned"}),403
        session['User']={"Name":username,"PR":Upr,"reg":Uinf}
        return jsonify({"message":"[Login] Succeed."}),200
    return (jsonify({"message":"ErRor.ApI"}),500)

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        if not('username' in request.form and 'password' in request.form):
            return jsonify({"message":"Register failed:Invalid."}),417
        username=request.form['username']
        pwd=request.form['password']
        RegInf={"Name":username,"password":pwd}
        if username in Users:
            return jsonify({"message":"Register failed:Name Used."}),406
        if Sfg['application']=='public':
            Reg(Mf,RegInf)
            return jsonify({"message":"[Register] Succeed."}),200
        elif Sfg['application']=='audit':
            auditq=[]
            if Mf.exists("./data/.audit"):
                auditq=json.loads(Mf.readtext("./data/.audit",encoding='utf-8'))
                if not type(auditq)==type([]):
                    auditq=[]
            auditq.append(RegInf)
            Mf.writetext("./data/.audit",auditq)
            Cback(Fore.GREEN+"[Handle][Register] New application.")
            return jsonify({"message":"[Register] Succeed."}),202
        elif Sfg['application']=='whiteonly':
            return jsonify({"message":"Register: Invalid mode:whiteonly."}),501
        elif Sfg['application']=='verify':
            return jsonify({"message":"Register: Need verify."}),401
        else:
            return jsonify({"message":"Server Config Invalid."}),500
    else:
        return jsonify({"message":"ErRoR:POST"}),405

def run(__Mf : OSFS,__CBack):
    global Mf, Cback, Sfg, Users
    Mf=__Mf
    Sfg=json.loads(Mf.readtext("./.Sconfig"))
    Cback=__CBack
    Users=json.loads(Mf.readtext("./data/User/.inf"))
    app.run(debug=False,host=Sfg['ip'],port=Sfg['port'])

if __name__=="__main__": 
    sys.exit(0) #实际使用