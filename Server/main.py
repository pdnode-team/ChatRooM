import os, json, time, sys
from colorama import *
import threading, handle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, User, Audit, VerifyCode

init(autoreset=True)

engine = create_engine('sqlite:///chatroom.db', echo=False)
Session = sessionmaker(bind=engine)
db_session = Session()

class Command:
    def user(self, args):
        def lackerror():
            print(Fore.RED + "[user] Error: No args for user.")
            print(Fore.YELLOW + "[user] Inf: You can visit WIKI to get how to use 'user' command.")
        if len(args) == 0:
            lackerror()
            return

        def all(args=None):
            users = db_session.query(User).all()
            tmp = 0
            for user in users:
                if user.valid:
                    tmp += 1
                    print(f"{user.name}  {user.pg}")
            print(f"\ntotal:{tmp} valid user.")

        def getinf(args):
            if len(args) == 1:
                lackerror()
                return
            username = args[1]
            user = db_session.query(User).filter_by(name=username).first()
            if user:
                print(Fore.GREEN + f"[user] Information for user:{username}")
                print(f"Permissions:{user.prconfig}")
                print(f"RegisterInf:{user.register}")
                print(f"InGroup    :{user.group}")
            else:
                print(Fore.YELLOW + f"[user] Error: Not found {username}.")

        def audit(args=None):
            config_app = config['application']
            if config_app != "audit":
                print(Fore.YELLOW + "[Audit] Disable audit mode.")
                return
            audits = db_session.query(Audit).all()
            audiq2 = []
            print("[audit] List:")
            for entry in audits:
                print("     " + str(entry.info))
                a = input("     Allow?(T/F/C)")
                if a.upper() == 'T':
                    handle.Reg(db_session, entry.info)
                    db_session.delete(entry)
                elif a.upper() == 'F':
                    db_session.delete(entry)
                else:
                    audiq2.append(entry)
            db_session.commit()

        def verify(args):
            config_app = config['application']
            if config_app != "verify":
                print(Fore.YELLOW + "[Verify] Disable verify mode.")
                return
            verify_code = db_session.query(VerifyCode).first()
            if verify_code:
                print(f"[Verify] Verify:{verify_code.code}")
            if len(args) == 0:
                return
            if args[0] == "set":
                if len(args) < 2:
                    print(Fore.RED + "[Verify] Error: No verify code.")
                    return
                code = args[1]
                vc = db_session.query(VerifyCode).first()
                if vc:
                    vc.code = code
                else:
                    vc = VerifyCode(code=code)
                    db_session.add(vc)
                db_session.commit()
                print(Fore.GREEN + "[Verify] Set verify code successfully.")
            return

        def Register(args=None):
            RegInf = {}
            RegInf['Name'] = input("UserName:")
            RegInf['password'] = input("Password:")
            handle.Reg(db_session, RegInf)

        Clists = {"all": all, "getinf": getinf, "audit": audit, "register": Register, "verify": verify}
        argss = args[1:]
        if args[0] in Clists:
            Clists[args[0]](argss)
        else:
            print(Fore.RED + f"[user] Error: Invalid '{args[0]}'")

    def stop(self, args=None):
        print(Fore.GREEN + "[Server] Stopping...")
        os._exit(0)

    def __init__(self):
        self.List = {"stop": self.stop, 'user': self.user}

    def get(self, CI: str):
        CM = CI.split(" ")[0]
        args = CI.split(" ")
        del args[0]
        if not CM in self.List:
            print(Fore.RED + f"Error: No Command {CI}")
        else:
            try:
                self.List[CM](args)
            except Exception as Errorinf:
                print(Fore.RED + "[Command] " + str(Errorinf))

CMDList = Command()

def NewConfig():
    Sconfig = {}
    print(Fore.BLUE + "Welcome to use chatroom server service")
    print(Fore.YELLOW + "You haven't made config file for server.Now let set your server.")
    print("\n")
    Sconfig["ip"] = input(Fore.BLUE + "Server IP:") #Unsafe input way. /not_exist
    Sconfig["port"] = int(input(Fore.BLUE + "Server Port:"))
    Sconfig["application"] = input(Fore.BLUE + "Server application way:" + Fore.YELLOW + "[public/audit/whiteonly/verify]")
    Sconfig["showinf"] = (input(Fore.BLUE + "Server showinf:" + Fore.YELLOW + "[T/F]") == "T")
    Sconfig["log"] = (input(Fore.BLUE + "Server Log" + Fore.YELLOW + "[T/F]") == "T")
    with open("./.sconfig", "w", encoding="utf-8") as f:
        f.write(json.dumps(Sconfig, ensure_ascii=False))
    # 初始化数据库
    Base.metadata.create_all(engine)
    time.sleep(1)
    print(Fore.RED + "OK! Please restart main.py.")
    sys.exit(0)

def Load():
    try:
        global config
        with open("./.sconfig", "r", encoding="utf-8") as f:
            config = json.loads(f.read())
    except Exception as inf:
        print(Fore.RED + "Load config failed.\nPlease check your file.\nOr you can delete ./.Sconfig to reset.")
        sys.exit(0)

def Cback(o):
    print(o)

def Create_Server():
    global Server
    Server = threading.Thread(target=handle.run, daemon=True, args=(None, Cback))
    Server.start()
    print("Done!")
    try:
        while True:
            CI = input()
            CMDList.get(CI)
    except Exception as Errorinf:
        print(Fore.RED + "[Server ]" + str(Errorinf))
    finally:
        CMDList.get("stop")
    print() #nl

def main():
    if not os.path.exists("./.sconfig"):
        NewConfig()
    Load()
    try:
        Create_Server()
    except Exception as errorinf:
        pass #need inf

if __name__ == "__main__":
    main()