# 内存调试

内存调试和火焰图的生成逻辑略有差别。一般内存调试分为两类情况。

1. 内存泄漏。
2. 频繁申请释放内存。

前者是个bug，而后者是个性能问题（更适合放在栈上）。

前者对应的调试手段，一般是在可疑代码前捕捉一个snapshot，在可疑代码后再捕捉一个snapshot，在过程中始终记录每次堆上内存申请的执行栈和位置。对比两个snapshots，后者比前者多出来的内存，就是可疑泄漏内存。按照大小排序，然后再寻找分配时的执行栈，就知道当时分配的原因和是否应当释放。对所有多出来的内存进行分析后，就知道内存消耗的原因。

后者一般就是追踪每次申请内存的位置。如果一定时期内频繁内存申请和释放，执行栈还很类似，这个位置就很可疑。

## sort的使用

使用`python3 makedata.py <xxx>`，来生成一份随机的数据。

使用C对数据进行排序，`gcc -o sort-c sort-c.c`，随后`./sort-c <xxx>`。

使用Python对数据进行排序，`python3 sort.py <xxx>`。

使用Golang对数据进行排序，`go build sort-go.go`，随后`./sort-go <xxx>`。

# C语言内存调试

## valgrind

使用虚拟机追踪代码的全生命周期，所以程序会比正常慢个几十倍。

```
$ valgrind --leak-check=full --show-leak-kinds=all ./sort-c num 
==92230== Memcheck, a memory error detector
==92230== Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.
==92230== Using Valgrind-3.19.0 and LibVEX; rerun with -h for copyright info
==92230== Command: ./sort-c num
==92230== 
==92230== 
==92230== HEAP SUMMARY:
==92230==     in use at exit: 16,000,472 bytes in 2 blocks
==92230==   total heap usage: 4 allocs, 2 frees, 32,004,568 bytes allocated
==92230== 
==92230== 472 bytes in 1 blocks are still reachable in loss record 1 of 2
==92230==    at 0x48407B4: malloc (vg_replace_malloc.c:381)
==92230==    by 0x48CF1FA: __fopen_internal (iofopen.c:65)
==92230==    by 0x109253: main (in sort-c)
==92230== 
==92230== 16,000,000 bytes in 1 blocks are definitely lost in loss record 2 of 2
==92230==    at 0x48407B4: malloc (vg_replace_malloc.c:381)
==92230==    by 0x109227: main (in sort-c)
==92230== 
==92230== LEAK SUMMARY:
==92230==    definitely lost: 16,000,000 bytes in 1 blocks
==92230==    indirectly lost: 0 bytes in 0 blocks
==92230==      possibly lost: 0 bytes in 0 blocks
==92230==    still reachable: 472 bytes in 1 blocks
==92230==         suppressed: 0 bytes in 0 blocks
==92230== 
==92230== For lists of detected and suppressed errors, rerun with: -s
==92230== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

## heaptrace

非侵入工具，推测底层是gdb。方法也是拦截一系列内存调用，分析其中有哪些占用内存比较高。

```
$ heaptrack ./sort-c num
heaptrack output will be written to "heaptrack.sort-c.92945.zst"
/usr/lib/heaptrack/libheaptrack_preload.so
starting application, this might take some time...
heaptrack stats:
        allocations:            5
        leaked allocations:     3
        temporary allocations:  1
$ heaptrack --analyze "heaptrack.sort-c.92945.zst"
reading file "heaptrack.sort-c.92945.zst" - please wait, this might take some time...
Debuggee command was: ./sort-c num
finished reading file, now analyzing data:

MOST CALLS TO ALLOCATION FUNCTIONS
1 calls to allocation functions with 16.00M peak consumption from
main
  in sort-c
1 calls with 16.00M peak consumption from:

1 calls to allocation functions with 472B peak consumption from
__fopen_internal
  at ./libio/iofopen.c:65
  in /lib/x86_64-linux-gnu/libc.so.6
1 calls with 472B peak consumption from:
    main
      in sort-c
```

## memleak-bpfcc

ebpf的工具，非侵入式。其实是用uprobe挂载的C库的malloc等一系列函数。对于Python之类的高级语言作用有限。

```
$ sudo memleak-bpfcc -c './sort-c num'
Executing './sort-c num' and tracing the resulting process.
Attaching to pid 93467, Ctrl+C to quit.
[02:26:32] Top 10 stacks with outstanding allocations:
        4096 bytes in 1 allocations from stack
                0x00007f13d711e8cc      _IO_file_doallocate+0x8c [libc.so.6]
```

## mtrace

mtrace是libc的内置库，用于调试同样由libc提供的malloc和free。侵入式分析工具，使用时需要打开源码中的语句，重新编译（并带调试），再带环境变量执行。输出结果相比上面三个非侵入式工具，是最优美的。

```
$ gcc -g -o sort-c sort-c.c
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libc_malloc_debug.so MALLOC_TRACE="./mtrace.out" ./sort-c num
$ mtrace sort-c mtrace.out

Memory not freed:
-----------------
           Address     Size     Caller
0x0000555e4237b4a0    0x1d8  at ./libio/./libio/iofopen.c:67
0x00007fe10c8fb010 0xf42400  at sort-c.c:67
```

* [mtrace](https://man7.org/linux/man-pages/man3/mtrace.3.html)
* [Finding Memory Leaks Using mtrace](https://acmmac.acadiau.ca/finding_memory_leaks/articles/memory_leaks_mtrace.html)

# 调试Python内存使用

一般用到带gc语言，就很少有纯粹的“内存”泄漏问题。因为内存已经被runtime接管了。gc语言的问题，其实应该叫做“对象”泄漏。原因都是对象错误的保留引用，导致不能被释放。注意单纯的内存占用没有意义。因为从对象的释放，到内存清理和缩堆，中间可能有相当长时间间隔。

## tracemalloc

内置模块，侵入式分析工具，并不难用，直接看文档即可。行级追踪工具，所以能够精确到内存分配行。

```
$ python3 sort.py num
[ Top 10 differences ]
sort.py:25: size=106 MiB (+106 MiB), count=2974114 (+2974114), average=37 B
sort.py:27: size=7812 KiB (+7812 KiB), count=1 (+1), average=7812 KiB
sort.py:21: size=1024 B (+1024 B), count=11 (+11), average=93 B
/usr/lib/python3.11/tracemalloc.py:560: size=320 B (+320 B), count=2 (+2), average=160 B
/usr/lib/python3.11/tracemalloc.py:423: size=320 B (+320 B), count=2 (+2), average=160 B
sort.py:23: size=61 B (+61 B), count=1 (+1), average=61 B
<frozen codecs>:322: size=56 B (+56 B), count=1 (+1), average=56 B
```

* [tracemalloc](https://docs.python.org/3/library/tracemalloc.html)

## memory-profiler

同样是侵入式分析工具，用起来比tracemalloc略复杂一点。既要修改代码，同时启动时需要用模块加载代码执行。而且执行会比tracemalloc慢一点。

```
$ python3 -m memory_profiler sort.py num
Filename: sort.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    13     47.0 MiB     47.0 MiB           1   @profile
    14                                         def main():
    15     47.0 MiB      0.0 MiB           1       time.sleep(1)
    16                                         
    17                                             # import tracemalloc
    18                                             # tracemalloc.start()
    19                                             # ss1 = tracemalloc.take_snapshot()
    20                                         
    21    178.1 MiB    -15.1 MiB           2       with open(sys.argv[1]) as fi:
    22     47.0 MiB      0.0 MiB           1           l = []
    23    177.1 MiB      0.1 MiB     1000001           for line in fi:
    24    177.1 MiB      0.1 MiB     1000000               t = line.strip().split()
    25    177.1 MiB     61.2 MiB     1000000               t = tuple(map(int, t))
    26    177.1 MiB     68.7 MiB     1000000               l.append(t)
    27    193.3 MiB      1.0 MiB     2000001           l = sorted(l, key=lambda x: x[1])
    28                                         
    29                                             # ss2 = tracemalloc.take_snapshot()
    30                                             # top_stats = ss2.compare_to(ss1, 'lineno')
    31                                             # print("[ Top 10 differences ]")
    32                                             # for stat in top_stats[:10]:
    33                                             #     print(stat)
    34                                         
    35    178.1 MiB      0.0 MiB           1       time.sleep(10)
```

* [memprof](https://pypi.org/project/memprof/)

# 调试Golang内存使用

## runtime/pprof生成性能分析记录

runtime/pprof是golang内置的性能工具，属于入侵式工具。

```
$ go tool pprof out.perf
File: sort-go
Type: inuse_space
Entering interactive mode (type "help" for commands, "o" for options)
(pprof) top
Showing nodes accounting for 13.54MB, 100% of 13.54MB total
      flat  flat%   sum%        cum   cum%
   13.54MB   100%   100%    13.54MB   100%  main.main
         0     0%   100%    13.54MB   100%  runtime.main
(pprof) list main                                                                                                                                 Total: 13.54MB                                                                                                                                    ROUTINE ======================== main.main in sort-go.go
   13.54MB    13.54MB (flat, cum)   100% of Total                                                                                                          .          .     33:func main() {                                            
         .          .     34:   var is Items               
         .          .     35:   var item Item                                                                                                              .          .     36:                                                         
         .          .     37:   time.Sleep(1 * time.Second)            
         .          .     38:    
         .          .     39:   f, err := os.Open(os.Args[1])                                                                                              .          .     40:   if err != nil {                  
         .          .     41:           fmt.Println(err)                  
         .          .     42:           return                                                                                                             .          .     43:   }                                                     
         .          .     44:   defer f.Close()                         
         .          .     45:    
         .          .     46:   stream := bufio.NewReader(f)                          
         .          .     47:   line, err := stream.ReadString('\n')
         .          .     48:   for err == nil {
         .          .     49:           line = strings.TrimRight(line, "\n")
         .          .     50:           fields := strings.Split(line, " ")
         .          .     51:           item.data[0], _ = strconv.Atoi(fields[0])
         .          .     52:           item.data[1], _ = strconv.Atoi(fields[1])
   13.54MB    13.54MB     53:           is = append(is, item)
         .          .     54:           line, err = stream.ReadString('\n')
         .          .     55:   }
         .          .     56:
         .          .     57:   sort.Sort(is)
         .          .     58:
```
