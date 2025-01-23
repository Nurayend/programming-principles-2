import os
import os.path
def GetInfo():
    print("***Choose your command:")
    print("0 - exit")
    print("1 - work with a file")
    print("2 - work with a dir")
def FileInfo():
    print("***Choose your command:")
    print(" 0 - return to MainMenu")
    print(" 1 - delete file")
    print(" 2 - rename file")
    print(" 3 - add content to this file")
    print(" 4 - rewrite content of this file")
def DirInfo():
    print("***Choose your command:")
    print(" 0 - return to MainMenu")
    print(" 1 - rename dir")
    print(" 2 - number of files in it")
    print(" 3 - number of directories in it")
    print(" 4 - list content of the directory")
    print(" 5 - add file to this directory")
    print(" 6 - add new directory to this directory")
def FileManager():
    FileInfo()
    a = int(input())
    if a == 0:
        MainMenu()
    elif a == 1:
        name = input("Name of file(Delete):") + ".txt"
        try:
            os.remove(name)
        except FileNotFoundError:
            print("*This file doesn't exist*")
        else :print("*File was deleted*")
        FileManager()
    elif a == 2:
        name = input("Old file's name: ")+".txt"
        Nname = input("New file's name: ")+".txt"
        os.rename(name, Nname)
        print("*File name was changed*")
        FileManager()
    elif a == 3:
        name=input("File's name: ")+".txt"
        Open=open(name, "at")
        content = input("Your contetnt(Add): ")
        Open.write(content)
        Open.close()
        FileManager()
    elif a == 4:
        name=input("File's name: ")+".txt"
        Open=open(name, "wt")
        content = input("Your contetnt(rewrite):")
        Open.write(content)
        Open.close()
        FileManager()
def DirManager():
    DirInfo()
    a = int(input())
    if a == 0:
        MainMenu()
    elif a == 1:
        name = input("Old dir's name:")
        Nname = input("New dir's name:")
        try:
            os.rename(name, Nname)
        except FileNotFoundError:
            print("***This dir doesn't exist***")
        else :
            print("***Name was changed***")
        DirManager()
    elif a == 2:
        num = 0
        for f in os.listdir():
            File = os.path.join(f)
            if os.path.isfile(File):
                num+=1
        print("***Number of file is:", num)
        DirManager()
    elif a == 3:
        num = 0
        for f in os.listdir():
            Dir = os.path.join(f)
            if os.path.isdir(Dir):
                num+=1
        print("***Number of dir is:", num)
        DirManager()
    elif a == 4:
        for f in os.listdir():
            print(f)
        DirManager()
    elif a == 5:
        name = input("New file name: ") + ".txt"
        Open=open(name, "tw")
        Open.close()
        print("*File was created*")
        DirManager()
    elif a == 6:
        name = input("New dir's name: ")
        os.mkdir(name)
        print("***Dir was created***")
        DirManager()
def MainMenu():
    GetInfo()
    a=int(input())
    if a==0:
        return 0
    if a==1:
        FileManager()
    if a==2:
        DirManager()
MainMenu()