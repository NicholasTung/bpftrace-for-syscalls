# This script greps the kernel tree for the definition of each syscall,
# then puts data about its arguments into an easy-to-interact-with DataFrame
import pandas as pd
import subprocess

df = pd.DataFrame()

with open("syscalls_table.txt") as fp:
    lines = fp.readlines()
    ids, syscalls = list(), list()

    for line in lines:

        l = line.split("\t")
        ids.append(l[0])
        syscalls.append(l[2])

    df['syscall'] = syscalls
    print(df)
# Point this to your kernel source
# In my case, Arch doesn't have an easily browsable kernel,
# so I downloaded the source with Arch patches using the Arch Build System
KERNEL_TREE_DIR = r'/home/nicholast/build/linux/trunk/src/archlinux-linux'

# grep for each syscall in the syscall list
for syscall in syscalls:
    r = subprocess.run(
        'grep -rA3 -h "SYSCALL_DEFINE.\\?({},"'.format(syscall), # pattern to match syscall define functions
        shell=True,
        cwd=KERNEL_TREE_DIR,
        capture_output=True,
        text=True
    )

    # string cleaning
    s = str(r.stdout)
    s = s[:s.find(")") + 1].replace('\n', '').replace('\t', '')

    # Extract the part in between parentheses
    args = s[s.find("(") + 1:s.find(")")].split(",")

    # The first argument is the syscall itself
    args = args[1:]

    # strip whitespace
    args = [a.strip() for a in args]

    # List of arguments, type and name combined
    v = list()
    for i in range(0, len(args), 2):
        v.append("{} {}".format(args[i], args[i + 1]))

    # Index of the syscall that was found
    idx = df.index[df['syscall'] == syscall]

    # Add the arguments to the DataFrame
    for i in range(len(v)):
        df.loc[idx, 'arg{}'.format(i)] = v[i]

    print(df.loc[idx])
    print()

# Pickle it for later
print(df)
df.to_pickle("./syscalls.pkl")
