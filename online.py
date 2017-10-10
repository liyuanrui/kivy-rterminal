#coding=utf-8
import os
import sys
from fabric.api import env,run,put,output
pyhome=os.popen('echo $PYTHONHOME').read().strip()
os.chdir(pyhome)
env.hosts=['root@127.0.0.1:22']
env.password='12345678'
output['running']=False
output['status']=False
output['aborts']=False
env.output_prefix=False
def shell():
    run('python')#shell
def runfile(sfile):
    dfile=sfile.split('/')[-1]
    put(sfile,dfile)
    run('python %s && rm -rf %s'%(dfile,dfile))#run
if __name__ == '__main__':
    argv=[i for i in sys.argv if i]
    if len(argv) < 2:
        os.system('fab -f bin/online.py shell')
    else:
        os.system('fab -f bin/online.py runfile:%s'%argv[1])
# end