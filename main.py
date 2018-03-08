#coding=utf-8
#qpy:kivy
# -------------------------------------
#$PYTHONHOME/bin/online2.py
onlinePy='''
#coding=utf-8
import os,sys
from fabric.api import env,run,put,output
env.hosts=['{}']
env.password='{}'
output['running']=False
output['status']=False
output['aborts']=True
env.output_prefix=False
pyhome=os.popen('echo $PYTHONHOME').read().strip()
os.chdir(pyhome+'/bin')
def shell():run('{}')
    
def file(sfile):
    dfile=sfile.split('/')[-1]
    put(sfile,dfile)
    run('{} %s'%dfile)
    
if __name__ == '__main__':
    argv=[i for i in sys.argv if i]
    if len(argv) < 2:
        os.system('fab -f online2.py shell')
    else:
        os.system('fab -f online2.py file:%s'%argv[1])
'''

#$PYTHONHOME/bin/qpython-android5.sh A
qpython_android5='''
#!/system/bin/sh
DIR=${0%/*}
. $DIR/init.sh && $DIR/python-android5 "$@" && $DIR/end.sh
'''

#$PYTHONHOME/bin/qpython-android5.sh B
qpython_android6='''
#!/system/bin/sh
DIR=${0%/*}
. $DIR/init.sh && $DIR/python-android5 $DIR/online2.py "$@" && $DIR/end.sh
'''
# -------------------------------------

import os
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import WindowBase
from kivymd.theming import ThemeManager



def getconfig():
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/online2.py')
    if not os.path.exists(pyfile):
        with open(pyfile,'w') as f:
            f.write(onlinePy.format('pi@127.0.0.1:22','12345678','python','python'))
    with open(pyfile,'r') as f:r=f.read()
    hostname=re.findall("env\.hosts=\['(.*?)'\]",r)[0]
    password=re.findall("env\.password='(.*?)'",r)[0]
    command=re.findall("def shell\(\)\:run\('(.*?)'\)",r)[0]
    return hostname,password,command
    
    
def setconfig(hostname,password,command):
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/online2.py')
    pydro =os.path.join(pyhome,'bin/qpython-android5.sh')
    with open(pyfile,'w') as f:f.write(onlinePy.format(hostname,password,command,command))
    with open(pydro,'w') as f:f.write(qpython_android6)


def retconfig():
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/online2.py')
    pydro =os.path.join(pyhome,'bin/qpython-android5.sh')
    with open(pydro,'w') as f:
        f.write(qpython_android5)




def getstatus():
    pyhome=os.popen('echo $PYTHONHOME').read().strip()
    pyfile=os.path.join(pyhome,'bin/qpython-android5.sh')
    with open(pyfile) as f:r=f.read()
    if 'online2.py' in r:
        return True
    else:
        return False

    
class MyLayout(BoxLayout):
    def write(self):
        status=self.ids.status.text
        if 'Local' in status:
            hostname=self.ids.hostname.text
            password=self.ids.password.text
            command=self.ids.command.text
            setconfig(hostname,password,command)

            self.ids.status.text='Status: Remote'
            self.ids.action.text='run local'
        else:
            self.ids.status.text='Status: Local'
            self.ids.action.text='run remote'
            retconfig()


class MainApp(App):
    theme_cls=ThemeManager()
    def build(self):
        self.theme_cls.theme_style='Dark'
        return MyLayout()
    def on_start(self):
        status=getstatus()
        hostname,password,command=getconfig()
        self.root.ids.hostname.text=hostname
        self.root.ids.password.text=password
        self.root.ids.command.text=command
        if status:
            self.root.ids.status.text='Status: Remote'
            self.root.ids.action.text='run local'
        else:
            self.root.ids.status.text='Status: Local'
            self.root.ids.action.text='run remote'
        

if __name__=='__main__':
    MainApp().run()