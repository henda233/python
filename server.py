from socket import *
from threading import Thread
from time import sleep
'''Start'''
Ip="127.0.0.1"
Port=8888
MaxUser=10
Users = ["test"]
Password = ["123"]
Team = []
R_AdminUser="liguolin"
R_AdminPassword="zxc123"
MainText=''

Server = socket(AF_INET,SOCK_STREAM)
Server.bind((Ip,Port))
Server.listen(MaxUser)
print("Waiting for User...")

def SaveMes(info):
    global MainText
    MainText=MainText+info+"\n"
    with open('data.txt','w') as f:
        f.write(MainText)

def AdminAct(code,Who,socket):
    print("Someone is using Admin mode now!")
    if code == "Users":
        All=""
        for info in Team:
            All=All+str(info)+"\n"
        Mes = "Admin@|"+All
        socket.send(Mes.encode())
    if code == "ban":
        Team[int(Who)].close()
        Team.pop(int(Who))
        print( str(Team[int(Who)])+" has been baned.")
        Mes = "Mes@|Server|Someone has been baned!"
        SendText(Mes)



def CheckAdmin(A_user,A_password,socket):
    if A_user==R_AdminUser:
        if A_password==R_AdminPassword:
            Mes = "AdminLogin@|YES"
            socket.send(Mes.encode())
        else:
            Mes = "AdminLogin@|NO"
            socket.send(Mes.encode())
    else:
        Mes = "AdminLogin@|NO"
        socket.send(Mes.encode())


def ExitUser(socket):
    Team.remove(socket)
    socket.close()
    print(str(socket)+" has exited!")

def SendText(text):
    i=0
    NumOfTeam = len(Team)
    while i<=NumOfTeam-1:
        Team[i].send(str(text).encode())
        i=i+1

def SendinfoToAll(info):
    SaveMes(info)
    i=0
    NumOfTeam = len(Team)
    while i<=NumOfTeam-1:
        Team[i].send(str(info).encode())
        i=i+1
    Mes = str(info).split("|")
    print(Mes[1]+":"+Mes[2]+"\n")

def Res(R_User,R_Password,socket):
    Users.append(R_User)
    Password.append(R_Password)
    socket.send("Res@|Res sucessfully!".encode())
    print("A new one res!"+"\n"+"User:"+R_User+"\n"+"Password:"+R_Password+"\n")


def Login(L_User,L_Password,Socket):
    NumOfUser = len(Users)
    i=0
    while i<=NumOfUser-1:
        if L_User==Users[i]:
            if L_Password==Password[i]:
                Socket.send("Login@|Login".encode())
                print(str(Socket)+" Access sucessfully!")
            elif i==NumOfUser:
                Socket.send("Login@|No".encode())
        elif i == NumOfUser:
            Socket.send("Login@|No".encode())
        i=i+1

def TimeCheck(Socket,User):
    try:
        while 1:
            BTB="BTB@|GOING"
            Socket.send(BTB.encode())
            sleep(5)
    except:
        try:
            print("Someone has exited[BTB system].")
            Team.remove(Socket)
        except:
            pass


def CheckText(CText,Socket):
    if "Login@" in CText:
        Login_Text=str(CText).split("|")
        Login(Login_Text[1],Login_Text[2],Socket)
        print(str(Socket)+" Want to Login.")
        SaveMes(CText)
    if "Res@" in CText:
        Res_Text=str(CText).split("|")
        Res(Res_Text[1],Res_Text[2],Socket)
        SaveMes(CText)
    if "Mes@" in CText:
        SendinfoToAll(CText)
    if "Exit@" in CText:
        Exit_Text = str(CText).split("|")
        ExitUser(Socket)
        SaveMes(CText)
    if "AdminLogin@" in CText:
        AdminLogin_Text = str(CText).split("|")
        CheckAdmin(AdminLogin_Text[1],AdminLogin_Text[2],Socket)
        SaveMes(CText)
    if "Admin@" in CText:
        AdminActCode=str(CText).split("|")
        AdminAct(AdminActCode[1],AdminActCode[2],Socket)
        SaveMes(CText)


def GetRecDone(Socket,User):
    try:
        print(str(User)+" has joined server.")
        while 1:
            Temp = Socket.recv(1024)
            Text = Temp.decode()
            CheckText(Text,UserSocket)
    except:
        try:
            print(str(User)+" has exited server.")
            Team.remove(Socket)
        except:
            print("------------")


while 1:
    UserSocket,MUser=Server.accept()
    Th =Thread(target=GetRecDone,args=(UserSocket,MUser))
    Th.start()
    TimeTh = Thread(target=TimeCheck,args=(UserSocket,MUser))
    TimeTh.start()
    Team.append(UserSocket)