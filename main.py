from tkinter import *
import os
import shutil
from ctypes import windll
import string
import subprocess
import urllib.request
import extensions
#import requests

class FileExplorer():
    def __init__(self):
        self.main = Tk()
        self.main.title('File Explorer')
        self._dir = ""
        self.root = None
        self.Lb = None
        self.hasCopy = False
        self.copyPath = ""

        self.infoLabel = None
        self.infoText = ""

        if self._dir == "":  self._dir = "C:\\"

        menu=Menu(self.main, tearoff="off")
        self.main.config(menu=menu)

        file_menu= Menu(menu, tearoff="off")
        menu.add_cascade(label="File", menu=file_menu)
        new_menu = Menu(menu, tearoff="off")
        file_menu.add_cascade(label="New..", menu=new_menu)
        new_menu.add_command(label="Text file", command=lambda: extensions.text_file(self))
        file_menu.add_command(label="Open Explorer",command=self.openExplorer)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=self.main.destroy)

        net_menu= Menu(menu, tearoff="off")
        menu.add_cascade(label="Net", menu=net_menu)
        net_menu.add_command(label="Download from URL",command=self.downloadFile)
        net_menu.add_separator()
        net_menu.add_command(label="Show network info",command=lambda: extensions.netInfo(self))

        menu.add_command(label="Powershell",command=lambda: os.startfile("C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell_ise.exe"))
        
        
        
        self.renderFolder()


        self.main.mainloop()

    def changeInfo(self, info):
        self.infoText = info
        self.infoLabel.text = info
        self.renderFolder()
        self.infoLabel.update()
        self.main.update()
        self.main.update_idletasks()
        print(self.infoText)
        
    def change_file(self, event):
        if self._dir == "\\":
            self._dir = ""
        if self._dir != "":
            if os.path.isdir(self._dir + self.Lb.get(self.Lb.curselection())):
                self._dir = self._dir + self.Lb.get(self.Lb.curselection()) + "\\"
                self.renderFolder()
            else:
                os.startfile(os.path.join(self._dir, self.Lb.get(self.Lb.curselection())))
        else:
            self._dir = self.Lb.get(self.Lb.curselection())
            self.renderFolder()
        print("Changing dir to:", self._dir)
        
    def up(self, event=None):
        self._dir = "\\".join(self._dir.split("\\")[:-2]) + "\\"
        print("Changing dir to:", self._dir)
        #if "\\" not in _dir:    _dir += "\\"
        self.renderFolder()
        
    def delete(self, event):
        selection = self.Lb.get(self.Lb.curselection())
        self.changeInfo("Deleting...")
        print("Deleting", selection)
        if os.path.isfile(self._dir + self.Lb.get(self.Lb.curselection())):
            os.remove(os.path.join(self._dir, selection))
        else:
            shutil.rmtree(os.path.join(self._dir, selection))
        self.renderFolder()
        self.changeInfo("Done!")
        
    def copySelect(self, event):
        self.hasCopy = True
        self.copyPath = self._dir + "\\" + self.Lb.get(self.Lb.curselection())
        print("Copying:", self.copyPath)
        self.renderFolder()
        
    def paste(self, event):
        self.changeInfo("Pasting...")
        print("Pasting", self.copyPath, "in", self._dir)
        if os.path.isfile(self.copyPath):
            shutil.copy(self.copyPath, self._dir)
        else:
            print(self.copyPath, self._dir + "\\" + self.copyPath.split("\\")[-1])
            shutil.copytree(self.copyPath, self._dir + "\\" + self.copyPath.split("\\")[-1])
        self.renderFolder()
        self.changeInfo("Done!")
        
    def renderFolder(self, event=None):
        
        if self.root != None:    self.root.destroy()
        self.root = Frame(self.main)
        self.root.pack(fill=BOTH, expand=1)

        topBar = Frame(self.root)
        topBar.pack(fill=BOTH, expand=1)

        if self._dir != "\\":
            Label(topBar, text=self._dir, width=20).pack(side=LEFT, expand=1)
        else:
            Label(topBar, text="Select drive", width=20).pack(side=LEFT, expand=1)
        Button(topBar, text="<-", command=self.up).pack(side=RIGHT)
        Button(topBar, text="Set dir", command=self.directoryInput).pack(side=RIGHT)
        


        mainArea = Frame(self.root)
        mainArea.pack(fill=BOTH, expand=1)

        if self._dir != "\\":
            a = os.listdir(self._dir)
        else:
            alphabet = []
            for letter in range(97,123):
                alphabet.append(chr(letter).upper())

            a = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in alphabet:
                if bitmask & 1:
                    a.append(letter + ":\\")
                bitmask >>= 1

        if len(a) < 20:
            self.Lb = Listbox(mainArea, height=len(a))
        else:
            sb = Scrollbar(mainArea, orient=VERTICAL)
            sb.pack(side=RIGHT, fill=Y)
            self.Lb = Listbox(mainArea, height=20)
            self.Lb.configure(yscrollcommand=sb.set)
            sb.config(command=self.Lb.yview)
        
        for i in range(len(a)):
            self.Lb.insert(1, a[len(a)-i-1])
        self.Lb.pack(fill=BOTH, expand=1)
        self.Lb.select_set(0)
        self.Lb.focus_set()

        if self.hasCopy:
            Label(mainArea, text="Copied: "+self.copyPath).pack()
        else:
            Label(mainArea, text="Nothing copied").pack()
        if self.infoText == "":
            self.infoLabel = Label(mainArea, text="No operation in progress")
        else:
            self.infoLabel = Label(mainArea, text=self.infoText)
        self.infoLabel.pack()
            
        self.main.bind("<Return>", self.change_file)
        self.main.bind("<BackSpace>", self.up)
        self.main.bind("<Escape>", self.up)
        self.main.bind("<Delete>", self.delete)
        self.main.bind("<Control-r>", self.renderFolder)
        self.main.bind("<Control-c>", self.copySelect)
        self.main.bind("<Control-v>", self.paste)
        self.Lb.bind('<Double-1>', self.change_file)

    def directorySet(self, __dir, top):
        self._dir = __dir.get()
        if self._dir == "":  self._dir = "C:\\"
        top.destroy()
        self.renderFolder()
                                                 
    def openExplorer(self):
        #print(r'explorer /select,"' + _dir + '"')
        #subprocess.Popen(r'explorer /select,"' + _dir + "\\" + '"')
        os.startfile(self._dir)
        
    def directoryInput(self):
       top= Toplevel(self.main)
       top.attributes("-topmost", True)
       #top.geometry("750x250")

       entry= Entry(top, width= 20)
       entry.insert(END, self._dir)
       entry.pack()

       Button(top,text= "Set as directory", command= lambda:self.directorySet(entry, top)).pack()
                                                 
    def downloadFile(self):
        top= Toplevel(self.main)
        top.attributes("-topmost", True)
        Label(top, text="URL:").pack()
        entry= Entry(top, width= 20)
        entry.pack()
        Label(top, text="New file name:").pack()
        entry2= Entry(top, width= 20)
        entry2.pack()

        Button(top,text= "Download", command= lambda:self.download(entry, entry2, top)).pack()
        
    def download(self, url, filename, top):
        self.changeInfo("Downloading...")
        urllib.request.urlretrieve(url.get(), self._dir + filename.get())
        top.destroy()
        self.changeInfo("Done")

FileExplorer()
