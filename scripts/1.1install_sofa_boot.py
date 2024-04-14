### chdir
import os
CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
# chdir to the directory of this script
os.chdir(CUR_FDIR)
os.chdir("./sofa-boot-3.1.4")

# skip test
os.system("mvn clean install -DskipTests -Dmaven.javadoc.skip=true")