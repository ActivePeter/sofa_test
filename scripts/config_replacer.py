import os
import yaml

# chdir to the directory of this script
CUR_FPATH = os.path.abspath(__file__)
CUR_FDIR = os.path.dirname(CUR_FPATH)
os.chdir(CUR_FDIR)

import re

class FileReplacer:
    def __init__(self, config):
        self.config = config

    def replace_one(self,one):
        for file_config in one['files']:
            file_path = file_config['path']
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
            self.replace_one(one_replace)
        

if __name__ == "__main__":
    with open("config_replacer.yml", 'r') as file:
        config = yaml.safe_load(file)

    file_replacer = FileReplacer(config)
    file_replacer.replace_content()
