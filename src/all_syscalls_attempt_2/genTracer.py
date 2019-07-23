# Writes the .bt tracer using a table of syscalls
import pandas as pd

table = pd.read_pickle("./syscalls.pkl")
print(table.dtypes)

columns = list(table)
argsList = ["arg{}".format(i) for i in range(6)]

# for convenience dealing with the arguments
class SyscallArg:
    def __init__(self, combined):
        sp = combined.split()
        self.type = ' '.join(sp[:-1])
        self.name = sp[-1]

    def getPrintType(self):
        if "*" in self.type:
            return "%p"

        numTypes = ["int", "float", "long", "timer_t",
                    "u64", "key_serial_t", "size_t", "uid_t",
                    "s32", "u32", "clockid_t", "qid_t", "loff_t",
                    "gid_t", "off_t", "mqd_t", "key_t", "pid_t",
                    "rwf_t", "umode_t", "compat_ulong_t", "compat_size_t",
                    "aio_context_t"]
        if any(substring in self.type for substring in numTypes):
            return "%d"

        charTypes = ["char"]
        if any(substring in self.type for substring in charTypes):
            return "%c"

        return "%p"


# gets all the types of arguments 
# so that I can handle weird types defined in the kernel
# and use the correct print character
def getAllTypes():
    typeSet = set()

    for col in argsList:
        tempSet = {SyscallArg(a).type for a in table[col] if type(a) is str}
        typeSet = typeSet | tempSet

    with open("types.txt", "w") as file:
        for t in typeSet:
            file.write("{}\n".format(t))


# Notes: uname:newuname, stat:newstat, fstat:newfstat, lstat:newlstat, sendfile:sendfile64
def writeTracer():
    with open("trace.bt", "w") as bt:
        bt.write(
            """
            #!/usr/bin/env bpftrace

            BEGIN
            {
                printf("Tracing syscalls for something. Ctrl-C to stop.\\n");
                printf("%-9s %-6s %s \\n", "TIME", "PID", "EVENT");
                @start = nsecs;
            }
            """
        )

        for row in table.itertuples():
            syscall = str(row[1])
            args = [SyscallArg(str(row[i])) for i in range(2, 7)]

            bt.write(
                """
                tracepoint:syscalls:sys_enter_{} /comm == {}/
                {{
                    printf("%d µs:   ", (nsecs - @start)/1000);
                    printf("%-6d %-9s %15s ", pid, comm, probe);
                """.format(syscall, "str($1)")
            )

            args = [a for a in args if str(a.name) != 'nan']

            argFormatStrs = list()
            argStructAccessStrs = list()
            j = 0
            argFormatStrs.append("[{}]".format(len(args)))
            for arg in args:
                argFormatStrs.append(
                    "{}:{}".format(
                        argsList[j], arg.getPrintType()
                    )

                )
                argStructAccessStrs.append(" args->{}".format(arg.name))
                j += 1

            printArgs = """
                printf("{} \\n"{} {});
            }}
            """.format(
                " ".join(argFormatStrs),
                "," if len(argFormatStrs) > 1 else "",
                ",".join(argStructAccessStrs)
            )

            bt.write(printArgs)


def main():
    writeTracer()


if __name__ == "__main__":
    main()
