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

BPF_HASH(counts, int, u64, 256);
BPF_STACK(params, int, 256);
BPF_HASH(result, int, int, 256);

int fib(struct pt_regs *ctx, int n) {
	if (n >= 5) {
		counts.atomic_increment(n);
	}
	// u64 pid = bpf_get_current_pid_tgid();
	if (params.push(&n, 0) != 0) {
		return 0;
	}
	return 0;
}

int fibret(struct pt_regs *ctx) {
	int r = PT_REGS_RC(ctx);
	int n;
	if (params.pop(&n) != 0) {
		return 0;
	}

	// bpf_trace_printk("pid:%d, n: %d, r: %d", pid, n, r);
	result.update(&n, &r);
	return 0;
}
'''


def main():
    b = BPF(text=bpf_text)
    b.attach_uprobe(name="./fib", sym="fib", fn_name="fib")
    b.attach_uretprobe(name="./fib", sym="fib", fn_name="fibret")

    # while True:
    #     try:
    #         (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    #     except ValueError:
    #         continue
    #     print(ts, pid, msg)

    try:
        time.sleep(100)
    except KeyboardInterrupt:
        pass

    print('counts:')
    counts = b.get_table('counts')
    for k, v in counts.items():
        print(k, v)

    print('results:')
    result = b.get_table('result')
    for k, v in result.items():
        print(k, v)


if __name__ == '__main__':
    main()
