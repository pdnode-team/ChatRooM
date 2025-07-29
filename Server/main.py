from fs.osfs import *
import os,json,time,sys
from colorama import *
import socket,threading
import handle

init(autoreset=True)

class Command:
    def user(self,args):
        # data/User/{xxx}/
        # .prconfig (权限)
        # .register (注册信息)
        # .group (聊天群组)
        def lackerror():
            print(Fore.RED+f"[user] Error: No args for user.")
            print(Fore.YELLOW+f"[user] Inf: You can visit WIKI to get how to use \'user\' command.")
        if len(args) == 0:
            lackerror()
            return
        Inf=json.loads(Mf.readtext("./data/User/.inf"))
        def all():
            tmp=0
            for sj in Inf:
                if Inf[sj]["Valid"]==True:
                    tmp+=1
                    print(f"sj  {Inf[sj]["PG"]}") # PG:Permission groups
            print(f"\ntotal:{tmp} valid user.")
        def getinf():
            if len(args) == 1:
                lackerror()
                return
            if args[1] in Inf:
                print(Fore.GREEN+f"[user] Information for user:{args[1]}")
                print(f"Permissions:{json.loads(Mf.readtext(f"./data/User/{args[1]}/.prconfig"))}")
                print(f"RegisterInf:{json.loads(Mf.readtext(f"./data/User/{args[1]}/.register"))}")
                print(f"InGroup    :{json.loads(Mf.readtext(f"./data/User/{args[1]}/.group"))}")
            else:
                print(Fore.YELLOW+f"[user] Error: Not found {args[1]}.")
        def audit():
            if config['application'] != "audit":
                print(Fore.YELLOW+"[Audit] Disable audit mode.")
                return
            auditq=json.loads(Mf.readtext("./data/.audit"))
            audiq2=[]
            print("[audit] List:")
            for i in auditq:
                print("     "+str(i))
                a=input("     Allow?(T/F/C)")
                if(a.upper=='T'):
                    handle.Reg(Mf,i)
                elif a.upper=='F':
                    continue
                else:
                    audiq2.append(i)
            Mf.writetext("./data/.audit",audiq2)
        def Register():
            RegInf={}
            RegInf['Name']=input("UserName:")
            RegInf['password']=input("Password:")
            handle.Reg(Mf,RegInf)
            
        Clists={"all":all,"getinf":getinf,"audit":audit,"register":Register}
        if args[0] in Clists:
            Clists[args[0]]()
        else:
            print(Fore.RED+f"[user] Error: Invalid \'{args[0]}\'")
        
    def stop(self,args=None):
        print(Fore.GREEN+"[Server] Stopping...")
        os._exit(0)
    def __init__(self):
        self.List={"stop":self.stop,'user':self.user}
    def get(self,CI:str):
        CM=CI.split(" ")[0]
        args=CI.split(" ")
        del args[0]
        if not CM in self.List:
            print(Fore.RED+f"Error: No Command {CI}")
        else:
            try:
                self.List[CM](args)
            except Exception as Errorinf:
                print(Fore.RED+"[Command] "+str(Errorinf))
CMDList=Command()

def NewConfig():
    # .sconfig structment
    """
    {
        "ip":,
        "port":,
        "application":[public/audit/whiteonly/verify],
        "showinf":,
        "log":[1/0]
    }
    """
    Sconfig={}
    print(Fore.BLUE+"Welcome to use chatroom server service")
    print(Fore.YELLOW+"You haven't made config file for server.Now let set your server.")
    print("\n")
    Sconfig["ip"]=input(Fore.BLUE+"Server IP:") #Unsafe input way. /not_exist
    Sconfig["port"]=int(input(Fore.BLUE+"Server Port:"))
    Sconfig["application"]=input(Fore.BLUE+"Server application way:"+Fore.YELLOW+"[public/audit/whiteonly/verify]")
    Sconfig["showinf"]=(input(Fore.BLUE+"Server showinf:"+Fore.YELLOW+"[T/F]")=="T")
    Sconfig["log"]=(input(Fore.BLUE+"Server Log"+Fore.YELLOW+"[T/F]")=="T")
    Mf.writetext("./.sconfig",json.dumps(Sconfig,ensure_ascii=False))
    Mf.makedir("./data")
    Mf.makedir("./data/User")
    Mf.makedir("./data/Group")
    Mf.makedir("./data/Public")
    Mf.makedir("./data/Robot")
    Mf.makedir("./permissions")
    Mf.makedir("./log")
    Mf.writetext("./data/User/.inf",json.dumps({},ensure_ascii=False))
    time.sleep(1)
    print(Fore.RED+"OK! Please restart main.py.")
    sys.exit(0)

def Load():
    try:
        global config
        config=json.loads(Mf.readtext(".Sconfig",encoding="utf-8"))
    except Exception as inf:
        print(Fore.RED+"Load config failed.\nPlease check your file.\nOr you can delete ./.Sconfig to reset.")
        sys.exit(0)

def Cback(o):
    print(o)

def Create_Server():
    global Server
    Server=threading.Thread(target=handle.run,daemon=True,args=(Mf,Cback))
    Server.start()
    print("Done!")
    try:
        while(True):
            CI=input()
            CMDList.get(CI)
    except Exception as Errorinf:
        print(Fore.RED+"[Server ]"+str(Errorinf))
    finally:
        CMDList.get("stop")
    print() #nl

def main():
    global Mf
    Mf=OSFS(os.path.dirname(os.path.abspath(__file__)))
    if not Mf.exists("./.sconfig"):
        NewConfig()
    Load()
    try:
        Create_Server()
    except Exception as errorinf:
        pass #need inf    

if __name__ == "__main__":
    main()