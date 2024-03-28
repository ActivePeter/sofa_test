import os
import docker

CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)

# chdir to the directory of this script
os.chdir(CUR_FDIR)

os.system('docker-compose down')
os.system('docker-compose up  --force-recreate -d')

