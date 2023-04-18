from tkinter import *
import subprocess

def text_file(f):
    top= Toplevel(f.main)
    top.attributes("-topmost", True)
    Label(top, text="Name:").pack()
    entry= Entry(top, width= 20)
    entry.pack()
    Button(top,text= "Create", command= lambda:create_txt_file(entry, f, top)).pack()
def create_txt_file(e, f, top):
    open(f._dir + e.get()+".txt", "w+").close()
    top.destroy()
    f.renderFolder()

def netInfo(f):
    top= Toplevel(f.main)
    top.attributes("-topmost", True)
    data = subprocess.check_output(['ipconfig','/all']).decode('utf-8').split('\n')
    txt = ""
    _height = 1
    for item in data:
        i = item.split('\r')[:-1]
        if len(i) > 0:
            txt += str(item.split('\r')[:-1][0]) + "\n"
        else:
            txt+="\n"
        _height += 1

    #Label(top, text=txt, justify=LEFT).pack(anchor="w")

    w = Text(top, height=_height, borderwidth=0)
    w.insert(1.0, txt)
    w.pack()

    w.configure(state="disabled")

    # if tkinter is 8.5 or above you'll want the selection background
    # to appear like it does when the widget is activated
    # comment this out for older versions of Tkinter
    w.configure(inactiveselectbackground=w.cget("selectbackground"))
    
