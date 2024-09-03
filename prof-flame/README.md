# 概述

一般来说，生成火焰图都是两大步骤。

1. 生成性能分析记录。
2. 生成火焰图。

其中，生成性能分析记录有三大场景。

1. 直接执行目标代码，记录全生命周期数据。
2. 程序内编码开启，精准记录核心代码段。
3. 非侵入式，记录某个已存在的进程，某一段时刻。

# 例子

下面主要的例子，都是递归式计算fib数组。

# C下生成火焰图

## 使用perf生成性能分析记录

perf是一个常用的性能工具。在debian下，安装linux-perf工具包完成安装。

直接执行的情况。`sudo perf record -g -- python3 fib.py`

perf是非侵入式工具，所以没有程序内启动的选择。可以用`sudo perf record -g -p <pid>`，来跟踪运行中的进程。

## 生成火焰图

使用[这个项目](https://github.com/brendangregg/FlameGraph)，进行转换和统计。

安装请自行git clone。

0. chown perf.data
1. perf script > out.perf
2. stackcollapse-perf.pl out.perf > out.folded
3. flamegraph.pl out.folded > out.svg

## 使用ebpf生成性能分析记录

bpfcc-tools这个包下面有个工具，`/usr/sbin/profile-bpfcc`。这个工具使用ebpf做同样的事。同样是非侵入式工具。profile-bpfcc没有直接启动程序的选项。

使用`sudo /usr/sbin/profile-bpfcc -f -p <pid> > out.perf`抓取数据。数据和perf工具的folded兼容，所以用`flamegraph.pl out.perf > out.svg`，即可生成火焰图。

## 引用

* [如何读懂火焰图？](https://www.ruanyifeng.com/blog/2017/09/flame-graph.html)
* [Perf和火焰图](https://lgl88911.github.io/2020/03/19/Perf%E5%92%8C%E7%81%AB%E7%84%B0%E5%9B%BE/)
* [使用perf和火焰图分析系统性能](https://codertang.com/2018/12/17/perf/)
* [Flame Graphs](https://www.brendangregg.com/flamegraphs.html)
* [github](https://github.com/brendangregg/FlameGraph)

# Python下生成火焰图

## 通过cProfile生成性能分析记录

cProfile是python内置的性能工具，无需安装直接使用。

常见两类情况。一类是直接执行程序。第二类是程序内启动cProfile。cProfile不是非侵入式工具，所以没有非侵入执行这个选项。

直接执行的情况。直接用`python3 -m cProfile -o fib.prof fib.py`，就能获得完整记录。

[这个文档](https://docs.python.org/3/library/profile.html)也描述了如何在程序内，启动和停止profiling，导出文件的过程。以下是例子。

```
def main():
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    print(fib(35))
    pr.disable()
    pr.dump_stats('fib.prof')
```

## cProfile生成火焰图

cProfile的数据格式和perf不大一样，分析要用别的工具。安装包flameprof。执行`python3 -m flameprof fib.prof > fib.svg`，生成svg格式的火焰图。

## Python非侵入式工具

推荐austin。注意，不要通过apt安装。Debian的版本太老，无法支持debian自己的python3。用pip3去安装，可以获得3.6.0版。这个版本才能正常使用。

austin这个工具很有趣。本质上他和perf工具一样，是抓C的调试数据。但是austin通过抓出来的数据，还原了python栈。所以austin可以非侵入式的获得Python代码的执行分析记录。

直接执行程序，`austin -s -o out.perf python3 fib.py`。

针对已存在的进程，`austin -s -o out.perf -p <pid>`。

## austin的输出生成火焰图

austin的输出格式，和perf工具的folded兼容。所以直接用`flamegraph.pl out.perf > out.svg`，即可生成火焰图。

## Python的底层C火焰图

使用“C下生成火焰图”的工具，来分析Python，能得到C级别的火焰图。这是austin还原前的模样。有趣的是你用perf工具看一下fib.py的C火焰图，是不是哪里不对？和austin的图对不起来对吧。

这是因为Python对函数调用有优化。如果是Python函数调用Python函数，只变更内部结构，不增长C栈深度。所以利用C分析工具，来分析Python的运行时栈，得到的只有系统调用和`_PyEval_EvalFrameDefault`混合火焰图。所有Python内部代码的执行，都被打在了这个函数里。因而使用C工具分析Python运行时栈，一般没有意义。

## 引用

* [Python 程序性能分析和火焰图](https://xie.infoq.cn/article/74483a0917668dc17324d0313)
* [The Python Profilers](https://docs.python.org/3/library/profile.html)
* [flameprof](https://github.com/baverman/flameprof/)
* [austin](https://github.com/P403n1x87/austin)

# Golang下生成火焰图

## 示例代码的编译

题外话，怎么编译示例代码。`go build fib.go`

性能测试代码段可以按情况打开或关闭。

## runtime/pprof生成性能分析记录

runtime/pprof是golang内置的性能工具，属于入侵式工具，适配上面的场景2。下面是样例代码。

```
	f, err := os.Create("out.perf")
	if err != nil {
		log.Fatal("could not create CPU profile: ", err)
	}
	defer f.Close()

	if err := pprof.StartCPUProfile(f); err != nil {
		log.Fatal("could not start CPU profile: ", err)
	}
	defer pprof.StopCPUProfile()
```

## net/http/pprof生成性能分析记录

默认情况下，当你导入这个包，并且启动了http服务。这个包就自动导出一系列调试接口，便于调试。接口和上面的项目一一对应。注意直接对外暴露会造成安全隐患。

```
import _ "net/http/pprof"

go func() {
	log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

## pprof分析

一种是打开web界面，啥都有。`go tool pprof -http=0.0.0.0:8080 out.perf`

一种是使用cli界面。`go tool pprof out.perf`缺点就是需要输入命令来做许多分析。

# golang的底层C火焰图

同样，使用perf工具。这里没有任何幺蛾子，得到的结果和runtime/pprof差不多。

## 引用

* [Profiling Go Programs](https://go.dev/blog/pprof)
* [runtime/pprof](https://pkg.go.dev/runtime/pprof)
