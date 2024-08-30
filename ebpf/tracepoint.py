#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@date: 2024-08-26
@author: Shell.Xu
@copyright: 2024, Shell.Xu <shell909090@gmail.com>
@license: BSD-3-clause
'''
import time
import datetime

from bcc import BPF


bpf_text = '''
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

struct data_t {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
};
BPF_PERF_OUTPUT(events);

TRACEPOINT_PROBE(syscalls, sys_enter_openat)
{
	struct data_t data = {};
	data.pid = bpf_get_current_pid_tgid();
	data.ts = bpf_ktime_get_ns();
	bpf_get_current_comm(&data.comm, sizeof(data.comm));
	events.perf_submit(args, &data, sizeof(data));

	// char comm[TASK_COMM_LEN];
	// bpf_get_current_comm(comm, sizeof(comm));
	// bpf_trace_printk("from comm: %s", comm);
	return 0;
}
'''

b = BPF(text=bpf_text)


def print_event(cpu, data, size):
    event = b['events'].event(data)
    print(cpu, event.ts, event.pid, event.comm.decode('utf-8'))


def main():

    # while True:
    #     try:
    #         (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    #     except ValueError:
    #         continue
    #     print(ts, pid, msg)

    print('CPU   TS          PID     COMM')

    b["events"].open_perf_buffer(print_event)
    while True:
        try:
            b.perf_buffer_poll()
        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    main()
