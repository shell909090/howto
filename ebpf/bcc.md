# bcc快速入门

Debian为基础系统，安装bpfcc-tools和linux-headers-amd64。

* [Install](https://github.com/iovisor/bcc/blob/master/INSTALL.md)

# 基础使用案例

执行`python3 /usr/share/doc/bpfcc-tools/examples/tracing/hello_fields.py`。能跑即为安装成功。

其他例子在`/usr/share/doc/bpfcc-tools/examples/tracing/`下，请自行阅读。

# 实用工具

请参考`/usr/sbin/*_bpfcc`。

# uprobe跟踪C程序

1. `nm <exe>`
2. b = BPF(text=code)
3. b.attach_uprobe

我重点要说一下`PT_REGS_PARM1`这个宏。这个宏其实是拿di/edi。在x86_64架构的C调用里，这就是第一个参数。但是这个参数在返回时，确实可能被修改。有趣的是，我出问题的地方是一个多次的自调用递归，所以拿到的值始终是1/2，也就是递归最深处的参数。除了递归重设这个值外，再没有其他地方需要修改了。

解法也很粗糙。用一个`BPF_STACK`记录每次一调用，ret的时候拿最后一个参数就行。这样做问题也很明显——如果有两个进程并行执行，就可能出错。

# uprobe跟踪golang程序

其他没啥可说的。首先是根据文档[4]，不能跟踪uretprobe。其次，要拿参数不能用`PR_REG_PARM1`。用`objdump -d <exe>`反编译目标代码就可以知道，golang在调用时，参数放在ax/eax里。这时候反而要用`PT_REGS_RC`这个宏（变态啊）。

# 使用tracepoint跟踪kernel

1. `cat /sys/kernel/tracing/available_events`（kprobe是`/sys/kernel/tracing/available_filter_functions`）
   * `bpftrace -l 'tracepoint:*'`也行
   * `tplist-bpfcc`也行
2. 一般使用TRACEPOINT_PROBE来声明挂入点。
3. b = BPF(text=code)

# 参考和引用

1. [github](https://github.com/iovisor/bcc)
2. [Linux eBPF/bcc uprobes](https://www.brendangregg.com/blog/2016-02-08/linux-ebpf-bcc-uprobes.html)
3. [bcc Reference Guide](https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md)
4. [eBPF超乎你想象](https://kiosk007.top/post/ebpf%E8%B6%85%E4%B9%8E%E4%BD%A0%E6%83%B3%E8%B1%A1/)
5. [BPF Documentation](https://docs.kernel.org/bpf/)
6. [eBPF 开发实践教程：基于 CO-RE，通过小工具快速上手 eBPF 开发](https://eunomia.dev/zh/tutorials/)
