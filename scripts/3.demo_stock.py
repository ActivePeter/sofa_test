
### chdir
import os
CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
# chdir to the directory of this script
os.chdir(CUR_FDIR)

# output to crac_config
with open('crac_config', 'w') as f:
    fcontent ="""type: FILE
action: ignore
---
type: socket
action: ignore"""
    f.write(fcontent)


os.system('java -Djdk.crac.resource-policies=crac_config -XX:CRaCCheckpointTo=checkpoint-dir --add-opens java.base/java.lang=ALL-UNNAMED \
    -jar ../kc-sofastack-demo/stock-mng/target/stock-mng-0.0.1-SNAPSHOT.jar')