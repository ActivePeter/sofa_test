# pip3 install ruamel.yaml

import os
import yaml
import argparse
import sys
import pexpect

CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)

# chdir to the directory of this script
os.chdir(CUR_FDIR)

# first arg is the password
PASSWORD= ""

def run_cmd(cmd):
    print("> "+cmd)
    # if cmd.startswith("ssh") or cmd.startswith("scp"):
    #     # 创建spawn对象
    #     child = pexpect.spawn(cmd, encoding='utf-8',logfile=sys.stdout)

    #     # 匹配密码提示，然后发送密码
    #     child.expect('password:')
    #     child.sendline(PASSWORD)

    #     # 在这里可以继续与SSH会话进行交互
    #     # 例如，可以发送其他命令

    #     # 等待命令执行完成
    #     try:
    #         child.expect(pexpect.EOF)
    #     except:
    #         pass
    #     child.close()
    #     # 打印输出
    #     # print(child.before)
    # else:
    os.system(cmd)


def read_yaml(f):
    # parse
    import ruamel.yaml
    yaml = ruamel.yaml.YAML(typ='rt')
    parsed_data = yaml.load(f)

    return parsed_data

def entry():
    PASSWORD = sys.argv[1] if len(sys.argv)>1 else exit("Please provide password as the first argument.)")

    # read cluster-nodes.yml
    with open('node_config.yaml', 'r') as f:
        run_cmd("1.1install_basic.sh")

        # write to gen_ansible.ini
        ansible="[web]\n"

        # gen ssh key if not exist
        if not os.path.exists("/root/.ssh/id_rsa"):
            run_cmd("ssh-keygen -t rsa -b 2048")

        cluster_nodes = read_yaml(f)
        appeared_node={}
        for nid in cluster_nodes["nodes"]:
            node=cluster_nodes["nodes"][nid]
            ip=node["addr"]

            if ip not in appeared_node:
                ansible+="webserver{} ansible_host={} ansible_user=root\n".format(nid,ip)
                appeared_node[ip]=1

            run_cmd("ssh root@{} 'apt install python'".format(ip))
            run_cmd("ssh-copy-id root@{}".format(ip))
        
        # write to gen_ansible.ini, create if not exist
        with open("gen_ansible.ini","w") as f:
            f.write(ansible)
        

        # with open("gen_ansible.cfg","w") as f:
        #     f.write(
        #         "[defaults]\n"+\
        #         "inventory = ./gen_ansible.ini\n"+\
        #         "remote_user = root\n"+\
        #         "private_key_file = /root/.ssh/id_rsa\n"+\
        #         "host_key_checking = False"
        #     )
        
        # run ansible
        run_cmd("ansible -i gen_ansible.ini -m ping all")
        
entry()