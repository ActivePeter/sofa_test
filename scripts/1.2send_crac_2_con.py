### chdir
import os
CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
# chdir to the directory of this script
os.chdir(CUR_FDIR)
os.chdir("crac")

COMPILED_JDK_PATH='build/linux-x86_64-server-release/images/jdk/'
REMOTE_PORT=2222
REMOTE_PATH='root@192.168.31.96:/pvcdata/crac_jdk'

print(f"Ls jdk content: {COMPILED_JDK_PATH}")
os.system(f"ls {COMPILED_JDK_PATH}")

os.system(f"scp -r -P {REMOTE_PORT} {COMPILED_JDK_PATH} {REMOTE_PATH}")