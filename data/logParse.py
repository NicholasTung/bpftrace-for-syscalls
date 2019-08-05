# parse log files
# this may very well be some of the worst code ive ever written in my life
# but if it works, it works

import pandas as pd
import sys
import numpy as np

path = "{}/trial{}/".format(sys.argv[1], sys.argv[2])

with open("{}log.txt".format(path), 'r+') as f:
    lines = f.readlines()
    f.seek(0)
    f.truncate()
    f.writelines(lines[3:-3])
    lines = lines[3:-3]

    df = pd.DataFrame()
    timestamp, pid, process, syscall = list(), list(), list(), list()
    args = [list(), list(), list(), list(), list(), list()]

    for line in lines:
        if line.strip() == "":
            break

        l = line.split(maxsplit=6)

        timestamp.append(l[0])
        pid.append(l[2])
        process.append(l[3])
        syscall.append(l[4].split("_", maxsplit=3)[-1])

        a = [s.split(":")[-1] for s in l[-1].split()]
        numArgs = int(l[5][1])

        for i in range(numArgs):
            args[i].append(a[i])

        for i in range(numArgs, 6):
            args[i].append(np.nan)

    df["timestamp"] = timestamp
    df["pid"] = pid
    df["process"] = process
    df["syscall"] = syscall

    for i in range(len(args)):
        df["arg{}".format(i)] = pd.Series(args[i])


print(df)
df.to_pickle("{}df.pkl".format(path))
