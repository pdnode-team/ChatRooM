from fs.osfs import *
import os,json,time,sys
from colorama import *
import socket
import threading,asyncio

init(autoreset=True)

def NewConfig():
    # .sconfig structment
    """
    {
        "ip":,
        "port":,
        "application":[public/audit/whiteonly/verify],
        "showinf":,
        "maxlink":,
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
    Sconfig["maxlink"]=int(input(Fore.BLUE+"Server Maxlink:"))
    Sconfig["log"]=(input(Fore.BLUE+"Server Log"+Fore.YELLOW+"[T/F]")=="T")
    Mf.writetext("./.sconfig",json.dumps(Sconfig,ensure_ascii=False))
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

class TcpServer:
    def __init__(self):
        self.running=False
        self.Userlist={}
        self.server=None
    async def start_server(self):
        self.server = await asyncio.start_server(self.handle_client, Mf["ip"], Mf["port"])
        self.running = True
        async with self.server:
            await self.server.serve_forever()
    def handle_command(self):
        pass

def Create_Server():
    """
            首次加入服务器：["join","[serverip]",{"name":,"ip":,"MAC":,"Device":}]
            已经加入服务器: ["message",{"name":,"ip":,"MAC":,"Device":}]
            正常退出服务器: ["exit",{"name":,"ip":,"MAC":,"Device":}]
    """
    Server=TcpServer()
    CmdT=threading.Thread(target=Server.handle_command,daemon=True)
    CmdT.start()
    
    try:
        asyncio.run(Server.start_server())
    except:
        CmdT.join()
        pass

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