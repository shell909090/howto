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

int fib(struct pt_regs *ctx) {
	int n = PT_REGS_RC(ctx);
	if (n >= 5) {
		counts.atomic_increment(n);
	}
	return 0;
}
'''


def main():
    b = BPF(text=bpf_text)
    b.attach_uprobe(name="./fib", sym="main.fib", fn_name="fib")
    # golang不能用uretprobe，参考
    # https://kiosk007.top/post/ebpf%E8%B6%85%E4%B9%8E%E4%BD%A0%E6%83%B3%E8%B1%A1/
    # b.attach_uretprobe(name="./fib", sym="main.fib", fn_name="fibret")

    try:
        time.sleep(100)
    except KeyboardInterrupt:
        pass

    print('counts:')
    counts = b.get_table('counts')
    for k, v in counts.items():
        print(k, v)


if __name__ == '__main__':
    main()
