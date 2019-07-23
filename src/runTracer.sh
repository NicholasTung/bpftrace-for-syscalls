#!/bin/bash
if [ "$1" == "" ]; then
	echo 1>&2 "Missing process to trace"
	exit 128
elif [ "$2" != "" ]; then
	bpftrace trace.bt \
	-I /usr/lib/modules/$(uname -r)/build/include/uapi/linux \
	-I /usr/lib/modules/$(uname -r)/build/include/linux \
	$1 2>&1 | tee $2
else
	bpftrace trace.bt \
	-I /usr/lib/modules/$(uname -r)/build/include/uapi/linux \
	-I /usr/lib/modules/$(uname -r)/build/include/linux \
	$1
fi