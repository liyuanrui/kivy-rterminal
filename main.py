#coding=utf-8
#qpy:kivy

import os
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import WindowBase
from kivymd.theming import ThemeManager


def readsettings():
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/online.py')
    if os.path.exists(pyfile):
        with open(pyfile) as f:
            r=f.read()
        hostname=re.findall("env.hosts=\['(.*?)'\]",r)[0]
        password=re.findall("env.password='(.*?)'",r)[0]
        shellcommand=re.findall("run\('(.*?)'\)#shell",r)[0]
        runcommand=re.findall("run\('(.*?) \%s && rm -rf \%s'%\(dfile,dfile\)\)#run",r)[0]
    else:
        hostname='root@127.0.0.1:22'
        password='passwd'
        shellcommand='python'
        runcommand='python'
    return hostname,password,shellcommand,runcommand

def writesettings(hostname,password,shellcommand,runcommand):
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/online.py')
    with open('online.py') as f:
        r=f.read()
    old_hostname=re.findall("env.hosts=\['.*?'\]",r)[0]
    old_password=re.findall("env.password='.*?'",r)[0]
    old_shellcommand=re.findall("run\('.*?'\)#shell",r)[0]
    old_runcommand=re.findall("run\('.*? \%s && rm -rf \%s'%\(dfile,dfile\)\)#run",r)[0]
    r=r.replace(old_hostname,"env.hosts=['%s']"%hostname.strip())
    r=r.replace(old_password,"env.password='%s'"%password.strip())
    r=r.replace(old_shellcommand,"run('%s')#shell"%shellcommand.strip())
    r=r.replace(old_runcommand,"run('"+runcommand.strip()+" %s && rm -rf %s'%(dfile,dfile))#run")
    with open(pyfile,'w') as f:
        f.write(r)
    
def writesh(status):
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile1=os.path.join(pyhome,'bin/qpython.sh')
    pyfile2=os.path.join(pyhome,'bin/qpython-android5.sh')
    if status:
        with open('new_qpython.sh') as f:
            r1=f.read()
        with open('new_qpython-android5.sh') as f:
            r2=f.read()
    else:
        with open('qpython.sh') as f:
            r1=f.read()
        with open('qpython-android5.sh') as f:
            r2=f.read()
    with open(pyfile1,'w') as f:
        f.write(r1)
    with open(pyfile2,'w') as f:
        f.write(r2)

def readsh():
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile1=os.path.join(pyhome,'bin/qpython.sh')
    pyfile2=os.path.join(pyhome,'bin/qpython-android5.sh')
    with open(pyfile1) as f:r1=f.read()
    with open(pyfile2) as f:r2=f.read()
    if 'online.py' in r1 and 'online.py' in r2:
        return True
    else:
        return False

    
class MyLayout(BoxLayout):
    def write(self):
        status=self.ids.status.text
        dutton=self.ids.action.text
        if 'local' in status:
            hostname=self.ids.hostname.text
            password=self.ids.password.text
            shellcommand=self.ids.shellcommand.text
            runcommand=self.ids.runcommand.text
            writesettings(hostname,password,shellcommand,runcommand)
            writesh(True)
            self.ids.status.text='Status: remote running'
            self.ids.action.text='run local'
        else:
            writesh(False)
            self.ids.status.text='Status: local running'
            self.ids.action.text='run remote'


class MainApp(App):
    theme_cls=ThemeManager()
    def build(self):
        self.theme_cls.theme_style='Dark'
        return MyLayout()
    def on_start(self):
        status=readsh()
        hostname,password,shellcommand,runcommand=readsettings()
        self.root.ids.hostname.text=hostname
        self.root.ids.password.text=password
        self.root.ids.shellcommand.text=shellcommand
        self.root.ids.runcommand.text=runcommand
        if status:
            self.root.ids.status.text='Status: remote running'
            self.root.ids.action.text='run local'
        else:
            self.root.ids.status.text='Status: local running'
            self.root.ids.action.text='run remote'
        

if __name__=='__main__':
    MainApp().run()