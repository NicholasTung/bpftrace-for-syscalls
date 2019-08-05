# parse log files
# this may very well be some of the worst code ive ever written in my life
# but if it works, it works

# Usage: python logParse.py [program name] [trial number]

import pandas as pd
import sys
import numpy as np
import re

path = "{}/trial{}/".format(sys.argv[1], sys.argv[2])

with open("{}log.txt".format(path), 'r+') as f:

    df = pd.DataFrame()
    timestamp, pid, process, syscall, numArgs = list(), list(), list(), list(), list()
    args = [list(), list(), list(), list(), list(), list()]

    lineNum = 0
    errored = False
    for line in f:
        if line.strip() == "":
            break

        lineNum += 1

        try:
            tokens = line.split()
            lineArgs = list()

            for token in reversed(tokens):
                if re.fullmatch(r"arg\d:.*", token):
                    lineArgs.insert(0, token.split(":")[-1])
                elif re.fullmatch(r"\[\d\]", token):
                    argNum = int(token[1])
                    numArgs.append(argNum)
                elif re.fullmatch(r"tracepoint:syscalls:sys_enter.*", token):
                    syscall.append(token.split("_", maxsplit=2)[-1])
                elif re.fullmatch(r"\d+", token):
                    pid.append(token)
                elif re.fullmatch(r"µs:", token):
                    timestamp.append(tokens[tokens.index(token) - 1])
                    break
                else:
                    process.append(token)

            if len(timestamp) < lineNum:
                timestamp.append(np.NaN)
            if len(pid) < lineNum:
                pid.append(np.NaN)
            if len(process) < lineNum:
                process.append(np.NaN)
            if len(syscall) < lineNum:
                syscall.append(np.NaN)
            if len(numArgs) < lineNum:
                numArgs.append(np.NaN)

            for i in range(argNum):
                args[i].append(lineArgs[i])

            for i in range(argNum, 6):
                args[i].append(np.nan)

        except:
            print("{}: {}".format(lineNum, line))
            print(sys.exc_info())
            errored = True

    if errored:
        exit()

    df["timestamp"] = timestamp
    df["pid"] = pid
    df["process"] = process
    df["syscall"] = syscall
    df["numArgs"] = numArgs

    for i in range(len(args)):
        df["arg{}".format(i)] = pd.Series(args[i])


print(df)
df.to_pickle("{}df.pkl".format(path))
