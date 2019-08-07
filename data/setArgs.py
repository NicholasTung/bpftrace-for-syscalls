# prints all syscalls, with a set of each of its arguments
# Usage: python setArgs.py [program name] [trial number]
import pandas as pd
import sys


def main():
    path = "{}/trial{}/".format(sys.argv[1], sys.argv[2])

    df = pd.read_pickle("{}df.pkl".format(path))

    usedSyscalls = tuple(df["syscall"].unique())

    print("Process: {}".format(sys.argv[1]))
    print("Number of unique syscalls: {}".format(len(usedSyscalls)))
    print()

    for syscall in usedSyscalls:
        syscallDF = df.loc[df["syscall"] == syscall]
        numArgs = syscallDF["numArgs"].iloc[0]

        print("{}():".format(syscall))
        print("# of calls: {}".format(len(syscallDF.index)))

        for i in range(numArgs):
            print("arg{}: {}".format(
                i, tuple(syscallDF["arg{}".format(i)].unique()))
            )

        print()


if __name__ == '__main__':
    main()
