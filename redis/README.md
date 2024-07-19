# redis四种模式

redis有三种高可用模式，主从，哨兵，集群。加上单节点，总共四个模式。

# 单节点

运行`make single`启动。

客户端连接可以运行`docker run -it --rm redis:7-alpine redis-cli -h <YOUR HOST IP>`，也可以`./redis-cli -h <YOUR HOST IP>`。

运行`docker stop redis`和`docker rm redis`，停止服务并删除实例。

# 主从

修改slave/redis.conf中的IP设定，从你自己的host ip里复制。

运行`make master-slave`启动。

客户端运行`./redis-cli -h <YOUR HOST IP>`连接master节点，运行`./redis-cli -h <YOUR HOST IP> -p 6378`连接slave节点。

在master节点上set一个值，去slave节点可以看到。在slave节点无法set值。

关闭master节点，slave节点无法工作（因为replica-serve-stale-data）。执行`config set replica-serve-stale-data yes`，随后slave可以正常工作。

打开master，关闭slave，master正常工作不受影响。

运行`make stop-master-slave`，停止服务并删除实例。

# 哨兵

哨兵的逻辑非常怪异。本身是一主二从的集群，又跑了一个高可用的哨兵集群监控。当主挂掉后，哨兵集群会自动选举主，并且通过写配置的方法切过去。

由于哨兵的网络比较复杂，因此我直接用了`--net=host`。好孩子不要学。

运行`make sentinel`启动。

客户端运行`./redis-cli -h <YOUR HOST IP> -p 6377`连接master节点。6378和6379为slave节点。

关掉redis1，此时再连上6378，输入info可以看到，role已经是master了。（master也可能在6379）set数据也成功。

再启动redis1。刚开始能看到，role还是master，等一下role就变成slave了。刚刚在redis2上set的数据也能看到。这是哨兵更改了配置所致。

运行`make stop-sentinel`，停止服务并删除实例。

# 集群

集群就简单多了。

运行`make cluster`启动。下面会列出多个节点，输入yes，组建集群。

客户端运行`./redis-cli -h <YOUR HOST IP> -p 6377`连接cluster1节点。6378和6379为另外两个节点。输入info，三者的role均为master，且均可以set。但当数据的slot不在本实例时，会返回MOVED，引导你去正确的节点。

客户端运行`./redis-cli -h <YOUR HOST IP> -p 6377 -c`，以cluster模式运行，就可以随意set了。redis-cli会自动跟过去set。

关闭跟过去的节点（我这里是cluster3），再试图读写这个key就会报错。

运行`make stop-cluster`，停止服务并删除实例。
