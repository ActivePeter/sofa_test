### install library
import subprocess
import os
def install_library(library_name):
    try:
        # 使用subprocess调用命令行来运行pip install
        subprocess.check_call(["pip", "install", library_name])
        print(f"{library_name} 安装成功")
    except subprocess.CalledProcessError:
        print(f"无法安装 {library_name}，请手动安装")
libraries_to_install = ["mysql-connector-python", "pyyaml"]  # 替换为你需要安装的库列表
for library in libraries_to_install:
    install_library(library)


### chdir
import os
CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
# chdir to the directory of this script
os.chdir(CUR_FDIR)


### read config
import yaml
# 打开并读取YAML文件
with open('config.yaml', 'r') as file:
    # 加载YAML数据
    yamldata = yaml.safe_load(file)
MYSQL_HOST=yamldata['mysql_host']
MYSQL_PORT=yamldata['mysql_port']
MYSQL_USER=yamldata['mysql_user']
MYSQL_PASSWORD=yamldata['mysql_pw']


### utils
def os_system_sure(command):
    print(f"执行命令：{command}")
    result = os.system(command)
    if result != 0:
        print(f"命令执行失败：{command}")
        exit(1)
    print(f"命令执行成功：{command}")
import re
class FileReplacer:
    def __init__(self, config):
        self.config = config
    def replace_one(self,one_replace_key,one):
        for file_config in one['files']:
            file_path = file_config['path']
            print(f"replacing {one_replace_key} in {file_path}\n")
            appends=[]
            need_append='no_match_behaviour' in file_config and file_config['no_match_behaviour'] == 'append'
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    for matcher in file_config['matchers']:
                        pattern = re.escape(matcher).replace(r'\{\}', r'(.*)')
                        if not re.search(pattern, content):
                            if need_append:
                                line = matcher.format(one['value']) + '\n'
                                appends.append(line)
                        else:
                            content = re.sub(pattern, matcher.format(one['value']), content)
                with open(file_path, 'w') as file:
                    file.write(content)

            with open(file_path, 'a') as file:
                for append in appends:
                    print("> append",append)
                    file.write('\n'+append)
    def replace_content(self):
        for one_replace_key in self.config:
            one_replace=self.config[one_replace_key]
            self.replace_one(one_replace_key,one_replace)



### check mysql connection
import mysql.connector
from mysql.connector import Error
MYSQL_CON=None
def check_mysql_connection():
    global MYSQL_CON
    try:
        # 尝试连接到 MySQL 数据库
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        if connection.is_connected():
            print("成功连接到 MySQL 数据库")
            MYSQL_CON=connection
        else:
            print("无法连接到 MySQL 数据库")
            exit(1)

            # 可以执行其他操作或查询
            # 例如：cursor = connection.cursor()
            # 然后执行查询：cursor.execute("SELECT * FROM table_name")
    except Error as e:
        print(f"连接 Mysql 错误: {e}")
        exit(1)

        # # 确保关闭连接
        # if connection.is_connected():
        #     connection.close()
        #     print("连接已关闭")
check_mysql_connection()


### prepare sofa_registy
def prepare_sofa_registy():
    if os.path.exists("registry-all"):
        print("registry-all 文件夹已存在")
    else:
        print("registry-all 文件夹不存在, 开始下载")
        # check if the file exists
        if not os.path.exists("registry-all.tgz"):
            # print("registry-all.tgz 文件已存在")
            os_system_sure("wget https://github.com/sofastack/sofa-registry/releases/download/v6.1.9/registry-all.tgz")
        
        os_system_sure("tar -zxvf registry-all.tgz")

    if not os.path.exists("registry-all"):
        print("registry-all 准备失败")
        exit(1)

    os_system_sure("cp -f scripts_rsc/start_base.sh registry-all/bin/base/start_base.sh")
    print("registry-all 准备成功")
prepare_sofa_registy()


def prepare_sofa_boot():
    os_system_sure("python3 ./1.1install_sofa_boot.py")
prepare_sofa_boot()


### prepare demo prj
def prepare_demo_prj():
    if not os.path.exists("../kc-sofastack-demo"):
        os_system_sure("git clone https://github.com/ActivePeter/kc-sofastack-demo")

    if not os.path.exists("../kc-sofastack-demo"):
        print("kc-sofastack-demo 准备失败")
        exit(1)
    
    # update_config in prj
    FileReplacer({
        "replace_dbhost":{
            "value":f"{MYSQL_HOST}:{MYSQL_PORT}",
            "files":[
                {
                    "path":"../kc-sofastack-demo/stock-mng/src/main/resources/application.properties",
                    "matchers":[
                        "jdbc:mysql://{}/stock_db?characterEncoding=utf8"
                    ]
                },
                {
                    "path":"../kc-sofastack-demo/balance-mng/balance-mng-bootstrap/src/main/resources/application.properties",
                    "matchers":[
                        "spring.datasource.url=jdbc:mysql://{}/balance_db?characterEncoding=utf8",
                    ]
                }
            ]
        },
        "replace_dbpw":{
            "value":f"{MYSQL_PASSWORD}",
            "files":[
                {
                    "path":"../kc-sofastack-demo/stock-mng/src/main/resources/application.properties",
                    "matchers":["spring.datasource.password={}"]
                },
                {
                    "path":"../kc-sofastack-demo/balance-mng/balance-mng-bootstrap/src/main/resources/application.properties",
                    "matchers":["spring.datasource.password={}"]
                }
            ]
        },
        "replace_app_virtual_addr":{
            "value": "192.168.31.96",
            "files": [
                {
                    "path":"../kc-sofastack-demo/stock-mng/src/main/resources/application.properties",
                    "matchers":["com.alipay.sofa.rpc.virtual.host={}"],
                    "no_match_behaviour":"append"
                },
                {
                    "path":"../kc-sofastack-demo/balance-mng/balance-mng-bootstrap/src/main/resources/application.properties",
                    "matchers":["com.alipay.sofa.rpc.virtual.host={}"],
                    "no_match_behaviour":"append"
                }
            ]
        }
    }).replace_content()

    os.chdir("../kc-sofastack-demo")
    os_system_sure("mvn clean package -DskipTests")

    if MYSQL_CON.is_connected():
        try:
            cursor = MYSQL_CON.cursor()
            # 读取 SQL 文件内容
            with open("DDL.sql", 'r') as file:
                sql_script = file.read()
            # 执行 SQL 脚本
            cursor.execute(sql_script, multi=True)
            # MYSQL_CON.commit()
        except Error as e:
            print(f"执行 SQL 脚本错误: {e}")
    else:
        print("无法连接到 MySQL 数据库")
        exit(1)

    os.chdir("../scripts")
    
    print("kc-sofastack-demo 准备成功")
prepare_demo_prj()


    

    