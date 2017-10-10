#coding=utf-8
#qpy:console
__doc__ = """
run qpython online, the pythonic tool for remote execution and deployment

@version: 0.1
@Author: lr
"""
__title__ = "Run QPython Online"

import os,sys,zipfile,qpy
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
    cwget=checkmodule('wget')
    cmd=checkmodule('kivymd')
    mm=[]
    if cfabric:mm.append('fabric-qpython')
    if ckivy:mm.append('kivy-qpython')
    if cmd:mm.append('kivymd-qpython')
    if cwget:mm.append('wget')
    mm2=' and '.join(mm)
    
    msg = __doc__+"\n\n"\
        +"To run qpython online, you need install "+mm2+" and download github project qpython_run_online first"
    droid.dialogCreateAlert(__title__, msg)
    droid.dialogSetPositiveButtonText('OK')
    droid.dialogSetNegativeButtonText('NO')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    if response['which'] == 'positive':
        #droid.dialogCreateSpinnerProgress(title, "Installing ...")
        if cfabric:os.system(sys.executable+" "+sys.prefix+"/bin/pip install fabric-qpython -i  http://qpypi.qpython.org/simple  --extra-index-url  https://pypi.python.org/simple/")
        if ckivy:os.system(sys.executable+" "+sys.prefix+"/bin/pip install kivy-qpython -i  http://qpypi.qpython.org/simple  --extra-index-url  https://pypi.python.org/simple/")
        if cwget:os.system(sys.executable+" "+sys.prefix+"/bin/pip install wget")
        try:
            import wget
        except:
            os.system('python-android5 '+__file__)
            sys.exit()
        else:
            download()
        #droid.dialogDismiss()

        message = 'Ok, run kivy project qpython_run_online_master and set your host config'
        droid.dialogCreateAlert(__title__, message)
        droid.dialogSetPositiveButtonText('OK')
        droid.dialogShow()
        sys.exit()

    else:
        sys.exit()


def download():
    import wget
    url='http://github.com/liyuanrui/qpython_run_online/archive/master.zip'
    while True:
        try:
            zf=zipfile.ZipFile('qpython_run_online-master.zip','r')
            zf.close()
            break
        except:
            if os.path.exists('qpython_run_online-master.zip'):
                os.remove('qpython_run_online-master.zip')
            wget.download(url)

    zfile=zipfile.ZipFile('qpython_run_online-master.zip','r')
    zfile.extractall('projects')
    zfile.close()


try:
    import kivy
    import kivymd
    import fabric
    import wget
    os.chdir('projects/qpython_run_online-master')
except:
    first_welcome()
else:
    message = 'Ok, run kivy project qpython_run_online-master and set your host config'
    droid.dialogCreateAlert(__title__, message)
    droid.dialogSetPositiveButtonText('OK')
    droid.dialogShow()
    sys.exit()





