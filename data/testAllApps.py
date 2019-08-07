import os
import re
import subprocess
import sys


def main():
    print(sys.argv[1])
    apps = list()
    for d in os.scandir():
        if d.is_dir():
            apps.append(d.name)

    print(apps)
    for app in apps:
        numTrials = 0
        for t in os.scandir("{}/".format(app)):
            if re.fullmatch(r"trial\d", t.name):
                numTrials += 1

        for i in range(1, numTrials + 1):
            r = subprocess.run(["python", sys.argv[1], app, str(i)], capture_output = True, text = True)
            with open("{}/trial{}/{}.txt".format(app, i, sys.argv[1][:-3]), "w") as f:
                f.write(str(r.stdout))


if __name__ == '__main__':
    main()
