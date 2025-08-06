import sys, jwt, datetime, json, os
from flask import *
from colorama import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, User, Audit, VerifyCode

init(autoreset=True)

engine = create_engine('sqlite:///chatroom.db', echo=False)
Session = sessionmaker(bind=engine)
db_session = Session()

Cback = None
Sfg = None
app = Flask(__name__)
SECRET_KEY = os.urandom(24)

def Reg(db_session, RegInf: dict):
    # 注册用户
    user = User(
        name=RegInf['Name'],
        password=RegInf['password'],
        login=True,
        prconfig={"login": 1},
        register=RegInf,
        group={}
    )
    db_session.add(user)
    db_session.commit()

@app.before_request
def before_request():
    global Cback, Sfg
    if request.endpoint in ['home', 'login', 'register', 'register_verity']:
        return
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "[Server] Token missing."}), 400
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = data.get('username')
        user = db_session.query(User).filter_by(name=username).first()
        if not user:
            return jsonify({"message": "[Server] Invalid token."}), 406
        request.username = username
        token_permission = data.get('permission')
        local_permission = user.prconfig
        if token_permission is None or token_permission.get('login') != 1:
            return jsonify({"message": "[Server] Permission denied."}), 403
        if local_permission != token_permission:
            return jsonify({"message": "[Server] Invalid token."}), 403
        request.permission = local_permission
        request.reginf = user.register
        if data['reginf'] != request.reginf:
            return jsonify({"message": "[Server] Invalid token."}), 403
        if data['exp'] < datetime.datetime.utcnow():
            return jsonify({"message": "[Server] Token expired."}), 416
    except Exception:
        return jsonify({"message": "Token invalid."}), 401

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Chatroom.\nhttps://github.com/pdnode-team/ChatRooM"})

@app.route('/login', methods=['POST'])
def login():
    if not ('username' in request.form and 'password' in request.form):
        return jsonify({"message": "Login failed:Invalid."}), 417
    username = request.form['username']
    pwd = request.form['password']
    user = db_session.query(User).filter_by(name=username).first()
    if not user:
        return jsonify({"message": "Login failed:invalid username or password."}), 403
    if pwd != user.password:
        return jsonify({"message": "Login failed:invalid username or password."}), 403
    if not user.login:
        return jsonify({"message": "Login failed: Banned"}), 403
    token = jwt.encode({
        'username': username,
        'reginf': user.register,
        'permission': user.prconfig,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')
    return jsonify({"message": "[Login] Succeed.", "token": token}), 200

@app.route('/register', methods=['POST'])
def register():
    if not ('username' in request.form and 'password' in request.form):
        return jsonify({"message": "Register failed:Invalid."}), 417
    username = request.form['username']
    pwd = request.form['password']
    RegInf = {"Name": username, "password": pwd}
    user = db_session.query(User).filter_by(name=username).first()
    if user:
        return jsonify({"message": "Register failed:Name Used."}), 406
    if Sfg['application'] == 'public':
        Reg(db_session, RegInf)
        return jsonify({"message": "[Register] Succeed."}), 200
    elif Sfg['application'] == 'audit':
        audit_entry = Audit(info=RegInf)
        db_session.add(audit_entry)
        db_session.commit()
        if Cback:
            Cback(Fore.GREEN + "[Handle][Register] New application.")
        return jsonify({"message": "[Register] Succeed."}), 202
    elif Sfg['application'] == 'whiteonly':
        return jsonify({"message": "Register: Invalid mode:whiteonly."}), 501
    elif Sfg['application'] == 'verify':
        verify_code = db_session.query(VerifyCode).first()
        if not verify_code:
            return jsonify({"message": "Register: Need verify."}), 401
        return jsonify({"message": "Register: Need verify."}), 401
    else:
        return jsonify({"message": "Server Config Invalid."}), 500

@app.route('/register/<verify>', methods=['POST'])
def register_verity(verify):
    if Sfg['application'] != 'verify':
        return jsonify({"message": "Register: Invalid mode."}), 405
    verify_code = db_session.query(VerifyCode).first()
    if not verify_code:
        return jsonify({"message": "Register: No verify."}), 501
    if verify != verify_code.code:
        return jsonify({"message": "Register: Invalid verify."}), 406
    if not ('username' in request.form and 'password' in request.form):
        return jsonify({"message": "Register failed:Invalid."}), 417
    username = request.form['username']
    pwd = request.form['password']
    RegInf = {"Name": username, "password": pwd}
    user = db_session.query(User).filter_by(name=username).first()
    if user:
        return jsonify({"message": "Register failed:Name Used."}), 406
    Reg(db_session, RegInf)
    db_session.delete(verify_code)
    db_session.commit()
    return jsonify({"message": "[Register] Succeed."}), 200

def run(__Mf, __CBack):
    global Cback, Sfg
    Cback = __CBack
    
    with open("./.sconfig", "r", encoding="utf-8") as f:
        Sfg = json.loads(f.read())
    
    Base.metadata.create_all(engine)
    app.run(debug=False, host=Sfg['ip'], port=Sfg['port'])

if __name__ == "__main__":
    sys.exit(0)