import re
from datetime import datetime
from pprint import pprint

import yaml

start_app = "ActivityTaskManager: START u0"
stop_app = "Layer: Destroyed ActivityRecord"
lines = []
extract = {}


def parsing_file():
    with open('logcat_applications.txt', 'r') as file:
        for line in file:
            if start_app in line:
                lines.append(line)
            elif stop_app in line:
                lines.append(line)
    pprint(lines)


def extraction():
    for line in lines:
        time = re.search(r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', line)
        package = re.search(r"cmp=([\w./]+)", line)
        start_date = time.group(0)
        if package and time:
            app_path = package.group(1)
            app = 'application_{}'.format(len(extract) + 1)
            extract[app] = {"app_path": app_path, 'ts_app_started': start_date, 'ts_app_xclosed': None}
        else:
            if stop_app in line:
                pack = re.search(r"com.([\w.]+)", line)
                stop_date = time.group(0)
                path = pack.group(0)
                for applications in extract.items():
                    if path in applications[1]['app_path']:
                        applications[1]['ts_app_xclosed'] = stop_date

def yml():
    yml = yaml.dump(extract)
    file = open('output.yml', 'w')
    file.write(yml)
    file.close()
    return yml


def updated():
    pass


if __name__ == '__main__':
    parsing_file()
    extraction()
    yml()
