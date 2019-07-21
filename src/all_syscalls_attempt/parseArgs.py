# Utility functions to handle the string representing each argument
# of a syscall

def getType(arg):
    splitArg = arg.split()

    seperator = ' '

    return seperator.join(splitArg[:-1])


def getVar(arg):
    return arg.split()[-1]


# Returns the format specifier for a given argument
# Could definitely be improved
def getPrintType(arg):
    if "*" in getVar(arg):
        return "%p"

    numTypes = ["int", "float", "long", "timer_t",
                "u64", "key_serial_t", "size_t", "uid_t",
                "s32"]
    if any(substring in getType(arg) for substring in numTypes):
        return "%d"

    charTypes = ["char"]
    if any(substring in getType(arg) for substring in charTypes):
        return "%c"

    return "%p"


# variable name used to get it from the "args" struct
def getCallVar(arg):
    var = getVar(arg)
    if "**" in var:
    	var = var[2:]
    if "*" in var:
        var = var[1:]
    if "[]" in var:
    	var = var[:-2]
    return var


def fixSyscall(name):
    if "sys_" in name:
        return name[4:]

    return name
