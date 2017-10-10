#coding=utf-8
#qpy:console
__doc__ = """
run qpython online, the pythonic tool for remote execution and deployment

@version: 0.1
@Author: lr
"""
__title__ = "Run QPython Online"

import os,sys,zipfile,qpy,urllib2
from contextlib import closing
ROOT    = "/sdcard/qpython"
os.chdir(qpy.home)

try:
  import ssl
  ssl._create_default_https_context = ssl._create_unverified_context
except:
  pass
  
  
try:
    import androidhelper
    droid = androidhelper.Android()
except:
    pass

def checkmodule(module):
    try:
        exec('import %s'%module)
        return False
    except:
        return True

def first_welcome():
    cfabric=checkmodule('fabric')
    ckivy=checkmodule('kivy')
    cmd=checkmodule('kivymd')
    mm=[]
    if cfabric:mm.append('fabric-qpython')
    if ckivy:mm.append('kivy-qpython')
    if cmd:mm.append('kivymd-qpython')
    mm2=' and '.join(mm)
    
    msg = __doc__+"\n\n"\
        +"To run qpython online, you need install "+mm2+" and download github project qpython_run_online first"
    droid.dialogCreateAlert(__title__, msg)
    droid.dialogSetPositiveButtonText('OK')
    droid.dialogSetNegativeButtonText('NO')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    if response['which'] == 'positive':
        if cfabric:os.system(sys.executable+" "+sys.prefix+"/bin/pip install fabric-qpython -i  http://qpypi.qpython.org/simple  --extra-index-url  https://pypi.python.org/simple/")
        if cmd:os.system(sys.executable+" "+sys.prefix+"/bin/pip install kivymd-qpython -i  http://qpypi.qpython.org/simple  --extra-index-url  https://pypi.python.org/simple/")
        if ckivy:os.system(sys.executable+" "+sys.prefix+"/bin/pip install kivy-qpython -i  http://qpypi.qpython.org/simple  --extra-index-url  https://pypi.python.org/simple/")
        download()

        message = 'Ok, run kivy project qpython_run_online_master and set your host config'
        droid.dialogCreateAlert(__title__, message)
        droid.dialogSetPositiveButtonText('OK')
        droid.dialogShow()
        sys.exit()

    else:
        sys.exit()


def download():
    url='http://github.com/liyuanrui/qpython_run_online/archive/master.zip'
    with closing(urllib2.urlopen(url)) as h:
        r=h.read()
        with open('qpython_run_online-master.zip','wb') as f:
            f.write(r)

    zfile=zipfile.ZipFile('qpython_run_online-master.zip','r')
    zfile.extractall('projects')
    zfile.close()


try:
    import kivy
    import kivymd
    import fabric
    os.chdir('projects/qpython_run_online-master')
except:
    first_welcome()
else:
    message = 'Ok, run kivy project qpython_run_online-master and set your host config'
    droid.dialogCreateAlert(__title__, message)
    droid.dialogSetPositiveButtonText('OK')
    droid.dialogShow()
    sys.exit()





