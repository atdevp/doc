# 理论
<!-- TOC -->

- [理论](#%e7%90%86%e8%ae%ba)
  - [http](#http)
    - [状态码](#%e7%8a%b6%e6%80%81%e7%a0%81)
    - [Header](#header)
  - [性能](#%e6%80%a7%e8%83%bd)
    - [磁盘IO瓶颈](#%e7%a3%81%e7%9b%98io%e7%93%b6%e9%a2%88)

<!-- /TOC -->

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
### 磁盘IO瓶颈
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
avgrq-sz:平均每次设备io操作的数据大小
avgqu-sz:平均io队列长度
await:   平均每次io操作的等待时间ms
r_await: 平均每次读io操作的等待时间ms
w_await: 平均每次写io操作的等待时间ms
svctm:   平均每次设备io操作的服务时间
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

