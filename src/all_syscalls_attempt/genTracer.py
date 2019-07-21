# Please excuse debug prints and general poor code quality
# also in retrospect I could have just put the parseArgs functions in here
# Oh well

import parseArgs
import pandas as pd

table = pd.read_pickle("./table.pkl")
print(table.loc[table["Number"] == 174])
print()
print(table.dtypes)

columns = list(table)
argsList = ["arg{}".format(i + 1) for i in range(6)]

# This part was just to get all of the types for arguments, 
# so that I could handle them properly when printing them
typeSet = set()

for col in argsList:
    tempSet = {parseArgs.getType(a) for a in table[col] if type(a) is str}
    typeSet = typeSet | tempSet

with open("types.txt", "w") as file:
    for t in typeSet:
        file.write("{}\n".format(t))

# change this to the process that is going to be traced
PROCESS = "readmeme"
# NOTE: must check for entere_xecveat in the generated tracer 
# because it just kind of appeared but isn't an available syscall

# this part is especially bad :)
with open("trace.bt", "w") as bt:
    bt.write(
        """
        #!/usr/bin/env bpftrace

        BEGIN
        {
            printf("Tracing syscalls for something. Ctrl-C to stop.\\n");
            printf("%-9s %-6s %s \\n", "TIME", "PID", "EVENT");
        }
        """
    )
    for row in table.itertuples():

        name = parseArgs.fixSyscall(row[2])
        arg1 = row[3]
        arg2 = row[4]
        arg3 = row[5]
        arg4 = row[6]
        arg5 = row[7]
        arg6 = row[8]

        bt.write(
            """
            tracepoint:syscalls:sys_enter_{} /comm == "{}"/
            {{
                time("%H:%M:%S  ");
                printf("%-6d %-9s %s \\n", pid, comm, probe);
            """.format(name, PROCESS)
        )

        args = [arg1, arg2, arg3, arg4, arg5, arg6]
        args = [x for x in args if str(x) != 'nan']

        print(name)
        print(args)
        argF = list()
        argStruct = list()
        j = 0
        for arg in args:
            argF.append("{}:{}".format(
                argsList[j], parseArgs.getPrintType(arg)))
            argStruct.append(" args->{}".format(parseArgs.getCallVar(arg)))
            j += 1

        printArgs = """
            printf("{} \\n"{} {});
        }}
        """.format(" ".join(argF), "," if len(argF) > 0 else "", ",".join(argStruct))

        bt.write(printArgs)
