# 理论

<!-- TOC -->

- [理论](#理论)
    - [tcp](#tcp)
        - [专业名词](#专业名词)
    - [http](#http)
        - [状态码](#状态码)
        - [Header](#header)
    - [性能](#性能)
        - [系统整体性能top](#系统整体性能top)
        - [内存瓶颈free](#内存瓶颈free)
        - [内存瓶颈vmstat](#内存瓶颈vmstat)
        - [磁盘IO瓶颈iostat](#磁盘io瓶颈iostat)
        - [监控CPU处理器的相关统计信息之mpstat](#监控cpu处理器的相关统计信息之mpstat)

<!-- /TOC -->
## tcp

### 专业名词
* CWND: 拥塞窗口。 负责控制单位时间内，数据发送端的报文发送数量。
* RTT: round-trip time 往返时延 。  在这个时间内，发送端只能发送cwnd个报文数量。 用cwnd/rtt 表示发送速度。用来控制非发送速度。
* SS: slow start 慢启动阶段。tcp刚开始传输的时候，速度是慢慢长起来的，当发生丢包的现象的时候，才会停止指数增长规律。
* CA: congestion avoid 拥塞避免阶段。当tcp数据发送方感知到有数据丢失时，会降低cwnd这个发送数据包的数量，此时的发送速度就会降低，cwnd会再次增长，但是不是

## http

### 状态码
```
200: ok
201: created ok
301: 永久重定向 
     response header： Location: new url
302: 临时重定向
     response header： Location: new url
304: 条件请求没有满足。cdn中非常常见。
     if-none-match & etag
     if-modified-since & last-modified
307: 临时重定向
     response header: Location: new url
400: 错误的请求
401: http验证失败
407: proxy connection  验证失败
403: 禁止访问
404: 访问的资源在服务器上找不到
405: no supported method
406: 客户端段请求的类型服务器资源不支持
408: 客户端请求超时， 服务器在规定的时间没没有接收完来源请求
412: 客户端请求体太大了 比如后端如果是ngx，可能调整参数client_body_max_size
413: 表示请求的url太长或者请求首部太大，比如后端如果是ngx，可能调整client_header_max_size、large_client_header_max_size
415 客户端上传的文件类型不能被服务器接收
500: 服务器自身内部错误
502: 代理或者网关服务器同后端源服务器获取到错误响应
503: service unavilable 后端服务临时无法请求请求，可能是压力太大，也有可能是主动限流了
504: gateway timeout  在代理服务器规定的时间内，后端源服务器没有处理完成
```

### Header
* 通用首部
```
connection:
accept:
accept-charset:
accept-language:
accept-encoding:
cookies: 
```

* 请求首部
```
if-modified-since:
if-none-match:
refer:
Host:
user-agent:


```

* 响应首部
```
last-modified:
etag:
cache-control:
content-type:
content-length:
content-encoding:
status:
expires:
server:
access-control-allow-origin:
access-control-allow-headers:
access-control-allow-methods:

```

## 性能
### 系统整体性能top
* 命令格式
  > top

  > 按大写M，表示按消耗内存从大到小排序

  > 按大写P，表示按消耗CPU从大到小排序

  > 按1 显示所有逻辑cpu核心状况

```
id: 如果很低，说明cpu空闲时间占比较低，存在cpu瓶颈
wa: 等待io的cpu时间百分比，过高，说明io存在瓶颈

top - 15:26:14 up 132 days,  3:56,  1 user,  load average: 27.33, 24.80, 23.36
Tasks: 151 total,   1 running, 150 sleeping,   0 stopped,   0 zombie
%Cpu(s): 93.4 us,  6.1 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.5 st
KiB Mem : 16268160 total,   175792 free, 15887320 used,   205048 buff/cache
KiB Swap: 16777212 total, 13967252 free,  2809960 used.    81156 avail Mem
```

### 内存瓶颈free
```
buffer: 接受的数据暂存buffer，异步落盘
cache:  缓存，从磁盘读出，放到cache，提高下次读取效率
```

### 内存瓶颈vmstat
* 命令格式
> [V] [-n] [delay [count]]
1. -V 打印版本
2. -n 周期性循环输出，输出的头部信息只显示一次
3. deplay 是两次输出之间的间隔
4. count 输出几次

* 案例1
```
[@abc_10_2 ~]# vmstat  -n 1 3
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 8434240  37000 242469072    0    0     1    43    0    0  2  1 97  0  0
 2  0      0 8432740  37000 242470896    0    0     0   343 44776 29615  2  1 97  0  0
 0  0      0 8431148  37000 242472496    0    0     0   118 43223 31910  2  1 97  0  0

1. 进程
r: 运行队列的进程数量
b: 等待io的进程数量

2. memory
swpd: 虚拟内存使用量
free: 可用内存大小
buff: 用于做缓冲的
cache:用于做磁盘缓冲的

3. swap
si: 每秒从交换区写到内存的大小
so: 每秒写入交换区的内存大小

4. io
bi: 每秒读取块数
bo: 每秒写入块数

5. system
in: 每秒中断数，包含时钟中断
cs: 每秒上下文切换次数

6. CPU(百分比表示)
us: 用户进程的cpu占用
sy: 系统进程的cpu占比
id: cpu空闲时间占比
wa: io等待时间占比

```


### 磁盘IO瓶颈iostat
* 基础
```
    iops: 单位时间内内系统能处理的io数量。一般以每秒处理多少io为计算单位。
    磁盘服务时间: 包含寻道时间+旋转时间+传输时间。
    寻道时间: 磁头移动到正确磁道的时间。目前磁盘的寻道时间为3ms-15ms。
    旋转时间: 盘片将请求数据的扇区移动到磁头下面的时间。旋转时间和磁盘的转速息息相关。转速越快，旋转时间越短。比如
    7200rpm转速的旋转时间大约为60*1000/7200/2=4.17ms
    10000rpm转速的旋转时间大约为60*1000/10000/2=3ms
    15000rpm转速的旋转时间大约为60*1000/15000/2=2ms
```

* 命令格式
  > iostat [参数] [时间] [次数]

* 功能
  > 通过iostat命令查看CPU 、网卡、磁盘等设备的活动状况、负载信息

* 命令参数
``` 
-c 显示cpu使用情况
-d 显示磁盘使用情况
-k 以kb为单位显示
-m 以mb为单位显示
-x 显示详细信息
```
* 案例1之显示设备负载
```
%user:   cpu处在用户模式下的时间百分比
%system: cpu处在系统模式下的时间百分比
%nice:   cpu处在带nice值下的用户模式时间百分比
%iowait: cpu等待输入输出完成时间的百分比
%idle:   cpu空间时间的百分比


[@CentOS_ab_10_2 ~]# iostat   -c   1  2
Linux 3.10.0-693.el7.x86_64 (CentOS_bx_10_20) 	2019年12月04日 	_x86_64_	(48 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           3.04    0.04    0.92    0.17    0.00   95.83

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.39    0.00    0.63    0.02    0.00   96.97
```
> 如果%iowait比较高，说明磁盘io存在瓶颈

* 案例2之显示磁盘io详情
```
rrqm/s:  每秒进行merge的读操作数 
wrqm/s:  每秒进行merge的写操作数
r/s:     每秒完成读i/o设备次数
w/s:     每秒完成写i/o设备次数
rkB/s:   每秒读的字节数
wkB/s:   每秒写的字节数
avgrq-sz:平均每次io操作的数据大小
avgqu-sz:平均io队列长度
await:   平均每次io操作的等待时间ms
r_await: 平均每次读io操作的等待时间ms
w_await: 平均每次写io操作的等待时间ms
svctm:   平均每次设备io操作的服务时间ms(服务时间=寻道时间 + 旋转时间 + 传输时间)
%util:   被io消耗的cpu占比

[@CentOS_ab_10_2 ~]# iostat  -d -x -k 1 2
Linux 3.10.0-693.el7.x86_64 (CentOS_bx_10_20) 	2019年12月04日 	_x86_64_	(48 CPU)

Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
sda               0.00     0.23    0.02    0.23     0.18     2.00    17.47     0.00    1.33   13.91    0.07   0.41   0.01
sdb               0.00     0.21   13.78   15.78   475.85  2871.96   226.46     0.04    1.38    0.65    2.02   0.22   0.66

Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
sda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
sdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
```
> 如果%util接近100%,说明产生的io请求过多，io子系统已经产生满负荷，该磁盘存在瓶颈

>如果await远大于svctm，说明io队列太长了，io响应太慢，需要进行必要优化

>如果avgqu-sz比较大，说明存在大量io在等待

* 显示TPS和设备吞吐量
```
tps: 设备每秒的传输次数
kB_read/s: 每秒从设备读取的数量
kB_wrtn/s: 每秒从设备写入的数量

kB_read: 读取的总数据量
kB_wrtn: 写入的总数据量


[@CentOS_bx_10_20 ~]# iostat -d -k 1 2
Linux 3.10.0-693.el7.x86_64 (CentOS_bx_10_20) 	2019年12月04日 	_x86_64_	(48 CPU)

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda               0.25         0.18         2.00   11184192  121987855
sdb              29.57       475.83      2871.93 29030542184 175216334687

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda               0.00         0.00         0.00          0          0
sdb               7.00         0.00       226.50          0        226

```


### 监控CPU处理器的相关统计信息之mpstat

* 案例1分析
```
%user: 用户级别进程占用cpu百分比
%nice: 拥有nice优先级的进程占用cpu百分比
%sys: 系统进程占用cpu百分比
%iowait: io等待占用的cpu百分比
%irp: 硬中断占用的cpu百分比
%soft: 软中断占用的cou百分比



[@CentOS_abc_10_2 /]# mpstat  -P ALL 1  3

平均时间:  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
平均时间:  all    9.70    0.00    1.02    0.65    0.00    0.14    0.00    0.00    0.00   88.49
平均时间:    0    8.33    0.00    0.67    0.00    0.00    1.33    0.00    0.00    0.00   89.67
平均时间:    1    6.64    0.00    1.66    0.00    0.00    0.33    0.00    0.00    0.00   91.36
平均时间:    2    7.36    0.00    0.67    1.34    0.00    0.00    0.00    0.00    0.00   90.64
平均时间:    3   14.38    0.00    1.34    0.00    0.00    0.00    0.00    0.00    0.00   84.28
平均时间:    4   16.39    0.00    1.00    0.00    0.00    0.00    0.00    0.00    0.00   82.61
平均时间:    5   12.33    0.00    0.67    0.00    0.00    0.33    0.00    0.00    0.00   86.67
平均时间:    6   12.75    0.00    1.34    0.34    0.00    0.00    0.00    0.00    0.00   85.57
平均时间:    7   10.10    0.00    2.36    5.72    0.00    0.00    0.00    0.00    0.00   81.82
平均时间:    8   22.33    0.00    1.67    1.00    0.00    0.00    0.00    0.00    0.00   75.00
平均时间:    9   15.33    0.00    2.00    0.67    0.00    0.33    0.00    0.00    0.00   81.67
平均时间:   10   11.41    0.00    2.35    2.35    0.00    0.00    0.00    0.00    0.00   83.89
平均时间:   11   10.00    0.00    1.33    0.33    0.00    0.00    0.00    0.00    0.00   88.33
平均时间:   12   11.00    0.00    1.00    0.33    0.00    0.33    0.00    0.00    0.00   87.33
平均时间:   13   11.45    0.00    1.35    0.00    0.00    0.00    0.00    0.00    0.00   87.21
平均时间:   14   16.05    0.00    1.34    1.34    0.00    0.33    0.00    0.00    0.00   80.94
平均时间:   15    7.97    0.00    1.00    0.33    0.00    0.00    0.00    0.00    0.00   90.70
平均时间:   16   11.71    0.00    0.67    0.00    0.00    0.00    0.00    0.00    0.00   87.63
平均时间:   17    5.39    0.00    0.67    0.00    0.00    0.00    0.00    0.00    0.00   93.94
平均时间:   18    1.00    0.00    0.33    0.00    0.00    0.00    0.00    0.00    0.00   98.67
平均时间:   19    3.99    0.00    0.66    0.33    0.00    0.00    0.00    0.00    0.00   95.02
平均时间:   20    3.33    0.00    0.33    1.33    0.00    0.00    0.00    0.00    0.00   95.00
平均时间:   21    4.33    0.00    0.33    0.00    0.00    0.00    0.00    0.00    0.00   95.33
平均时间:   22    4.00    0.00    0.67    0.00    0.00    0.00    0.00    0.00    0.00   95.33
平均时间:   23    6.00    0.00    0.33    0.00    0.00    0.00    0.00    0.00    0.00   93.67
```