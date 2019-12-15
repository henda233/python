from socket import *
from threading import Thread
from time import sleep

Ip="127.0.0.1"
Port=8888
Online ="0"# 1 online 0 offline 2 admin mode
User = ""



Client = socket(AF_INET,SOCK_STREAM)
Client.connect((Ip,Port))
print("Connected Sucessfully!")

def CheckAdmin(info):
    global Online
    if "YES" in info:
        Online = "2"
        print("You are admin now!"+"\n")
    elif "NO" in info:
        print("Admin login failed! Your password is wrong!"+"\n")


def AdminLogin():
    Admin_user = input("admin user:")
    Admin_password = input("Code:")
    Mes = "AdminLogin@|"+Admin_user+"|"+Admin_password
    Client.send(Mes.encode())

def AdminMode():
    global Online
    while 1:
        print("1:ban")
        print("2:exit admin mode")
        Code = input("number:")
        if Code == "1":
           Mes = "Admin@|Users|None"
           Client.send(Mes.encode())
           Baner = input("Who you want to ban:")
           Mes = "Admin@|ban|"+Baner
           Client.send(Mes.encode())
        if Code=="2":
            Online="0"


def Exit():
    Mes = "Exit@|"+User
    Client.send(Mes.encode())


def Res():
    Res_User = input("User:")
    Res_Password = input("Password:")
    Mes="Res@|"+Res_User+"|"+Res_Password
    Client.send(Mes.encode())
    print("Send Res to server...")

def LoginYes(Code):
    global  Online
    if Code == "Login":
        Online="1"
        print("\n"+"Login sucessfully!")
        print("Try to talk something!")
        Mes = "Mes@|"+User+"|has joined server."
        Client.send(Mes.encode())
    elif Code == "No":
        Online="0"
        print("Your Password is wrong!")

def CheckText(info):
    if "Login@" in info:#recv login
        Login_Text = str(info).split("|")
        LoginYes(Login_Text[1])
    if "Mes@" in info:
        Message = str(info).split("|")
        print("\n"+Message[1]+":"+Message[2]+"\n"+">>> ")#print user's mess
    if "Res@" in info:
        Res_Text = str(info).split("|")
        print("\n"+Res_Text[1])
    if "exit@" in info:
        Exit()
    if "AdminLogin@" in info:
        CheckAdmin(info)
    if "Admin@" in info:
        Mes = str(info).split("|")
        print("AdminModeMessage: "+Mes[1]+"\n")


def User_Login():# send login
    global User
    User = input("User:")
    Password = input("Password:")
    LoginText = "Login@|" + User + "|" + Password
    Client.send(LoginText.encode())

def Opc(COp):
    if COp == "1":
        User_Login()
    if COp=="2":
        Res()
    if COp=="3":
        AdminLogin()


def Act():
    sleep(0.5)
    Op=input("what you want to do[1:login 2:res 3:admin login 4:exit]:")
    Opc(Op)

def Recinfo():
    print("=========Start recv========="+"\n")
    try:
        while 1:
            Temp=Client.recv(1024)
            Text = Temp.decode()
            CheckText(Text)
    except:
        print("Something wrong!")

def Talk():

    Send = input()
    if "Help@" in Send:
        print("exit@:exit from server safely.")
        print("That's all!")
    Mes = "Mes@|"+User+"|"+Send
    Client.send(Mes.encode())


Recth = Thread(target=Recinfo)
Recth.start()

while 1:
    sleep(0.5)
    if Online == "0":
        Act()
    elif Online == "1":
        Talk()
    elif Online=="2":
        AdminMode()
