
### chdir
import os
CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
# chdir to the directory of this script
os.chdir(CUR_FDIR)


os.system("java  --add-opens java.base/java.lang=ALL-UNNAMED \
    -jar ../kc-sofastack-demo/balance-mng/balance-mng-bootstrap/target/balance-mng-bootstrap-0.0.1-SNAPSHOT.jar")