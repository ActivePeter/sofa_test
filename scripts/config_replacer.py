import os
import yaml

class FileReplacer:
    def __init__(self, config):
        self.config = config

    def replace_content(self):
        for item in self.config['replacer_host']:
            file_path = item['path']
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    for matcher in item['matchers']:
                        old_value = matcher.format(self.config['replacer_host']['value'])
                        content = content.replace(old_value, self.config['replacer_host']['value'])
                with open(file_path, 'w') as file:
                    file.write(content)
            elif 'no_match_behaviour' in item and item['no_match_behaviour'] == 'append':
                with open(file_path, 'a') as file:
                    for matcher in item['matchers']:
                        line = matcher.format(self.config['replacer_host']['value']) + '\n'
                        file.write(line)

if __name__ == "__main__":
    with open("config_replacer.yml", 'r') as file:
        config = yaml.safe_load(file)

    file_replacer = FileReplacer(config)
    file_replacer.replace_content()
