import re
from datetime import datetime
from pprint import pprint

start_app = "ActivityTaskManager: START u0"
stop_app = "Layer: Destroyed ActivityRecord"
lines = []
extract = {}


def parsing_file():
    with open('logcat_applications.txt', 'r') as file:
        for line in file:
            if start_app in line:
                lines.append(line)
            if stop_app in line:
                lines.append(line)


def extraction():
    for line in lines:
        time = re.search(r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', line)
        package = re.search("cmp=([\w\./]+)", line)
        start_date = time.group(0)
        if package and time:
            app = 'application{}'.format(len(extract) + 1)
            app_path = package.group(1)
            extract[app] = {"app_path": app_path, 'ts_app_started': start_date}
        if "/" in app_path:
            apps_value = app_path.split('/')[0]
            if apps_value and stop_app in line:
                stop_date = time.group(0)
                extract[app]['ts_app_closed'] = stop_date


    pprint(extract)


def updated():
    pass


if __name__ == '__main__':
    parsing_file()
    extraction()
