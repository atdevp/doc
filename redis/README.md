# Redis
<!-- TOC -->

- [Redis](#redis)
  - [Redis常见数据结构使用方法](#redis%e5%b8%b8%e8%a7%81%e6%95%b0%e6%8d%ae%e7%bb%93%e6%9e%84%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95)
  - [缓存策略](#%e7%bc%93%e5%ad%98%e7%ad%96%e7%95%a5)

<!-- /TOC -->
## Redis常见数据结构使用方法
1. String
> 常用命令 set、get、decr、incr、mget
2. Hash
> 常用命令 hset、hget、hgetall
3. List
> 常用命令 lpush、rpush、lpop、lrange
4. Set
> 常用命令 sadd、spop、smembers、sunion
5. SortList
> 常用命令 zadd、zrange、zrem、zcard

## 缓存策略
1. volatile-lru
> 从已设置过期的数据集中删除最近最少使用的key
2. volatile-ttl
> 从已设置过期的数据集中调出快要过期的key
3. volatile-random
> 从已设置过期的数据集中随机删除一个key
4. allkeys-lru
> 从所有的数据集中挑选出最近最少使用的key
5. allkeys-random
> 从所有的数据集中随机删除某个key
6. no-enviction 
> 禁止数据驱逐

