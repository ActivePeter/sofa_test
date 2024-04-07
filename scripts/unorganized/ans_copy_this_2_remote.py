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

os.system("ansible-playbook -vvv ans_copy_this_2_remote.yml -i gen_ansible.ini")

