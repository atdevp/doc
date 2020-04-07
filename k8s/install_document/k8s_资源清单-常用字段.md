
<!-- TOC -->

- [资源清单参数](#资源清单参数)
    - [必备参数](#必备参数)
    - [主要参数](#主要参数)

<!-- /TOC -->

## 资源清单参数

### 必备参数
字段名称 | 字段类型 | 含义 
---  | ---  | ---
version	|string	|k8s的api版本,目前基本v1, kubectl api-verions查询
kind	|string	|资源的类型和角色,比如Pod
metadata	|object	|固定值
metadata.name	|string	|元数据对象的名称，这里由我们编写，比如pod的名称
metadata.namespace	|string	|元数据对象的命名空间，由我们自身定义
metadata.labels	|object	|key & value 类型
spec	|object	|固定值
spec.containers[]	|list	|一个列表
spec.containers[].name	|string	|容器名称
spec.containers[].image	|string	|镜像名称


### 主要参数
字段名称 | 字段类型 | 含义 
---  | ---  | ---
spec.containers[].imagePullPolicy	|string	"|3个可选值，Always、Never、ifNotPresent Always: 一直尝试从仓库拉镜像 ；Never：一直使用本地镜像；ifNotPresent： 本地有就用本地，没有就拉，最好的选择"
spec.containers[].command[]	|list	|容器启动命令，数组可以指定多个，不指定就用Dockerfile里面的CMD定义
spec.containers[].args[]	|list	|启动参数
spec.containers[].workingDir	|string	|容器的工作目录
spec.containers[].ports[]	|list	|容器要用到的端口列表
spec.containers[].ports[].name	|string	|端口名称
spec.containers[].ports[].containerPort	|string	|容器需要监听的端口
spec.containers[].ports[].hostPort	|string	|容器所在主机需要监听的端口号，默认和容器自身监听的端口号相同，设置了这个，同主机就不能启动该容器的副本了，宿主机端口不能冲突啊
spec.containers[].ports[].protocol	|string	|端口协议。 tcp、udp两种，默认tcp
spec.containers[].env[]	|list	|环境变量列表
spec.containers[].env[].name	|string	|环境变量的key
spec.containers[].env[].value	|string	|环境变量的value
spec.containers[].resources	|object	|固定值，容器资源上限开始配置
spec.containers[].resources.limits	|object	|固定值，运行资源上限
spec.containers[].resources.limits.cpu	|string	|cpu限制，单位cores数，将用于docker run —cpu-shares参数
spec.containers[].resources.limits.memroy	|string	|内存限制,单位为M， G
spec.containers[].resources.requests	|string	|固定值，容器启动或调度时的限制设置
spec.containers[].resources.requests.cpu	|string	|cpu请求，单位cores数，容器启动的的初始化可用值
spec.containers[].resources.requests.memory	|string	|内存请求，单位M，G，容器启动时的初始化可用值

额外参数
字段名称 | 字段类型 | 字段含义
--- | --- | ---	
spec.restartPolicy	|string	|定义pod的重启策略，可选：Always、OnFailure、Never。默认Always。Always： pod一旦终止，不管是怎么终止的，立即重启 OnFailure:  容器正常退出，即退出码为0，不会重启，反之才会重启Never： kubelet将退出码告诉master，自己不会重启pod"
spec.nodeSelector	|object	|定义node的lable标签，key：value格式
spec.imagePullSecrets	|object	|定义pull镜像时，使用secret名称，格式: name: secretkey
spec.hostNetwork	|Bool	|是否使用主机网络，默认false。 true： 表示使用主机网络，不使用docker0网桥，同时设置true，无法在同一个宿主机启动副本
spec.initContainers[] |list | Pod中初始化容器，Main container依赖
spec.initContainers[].name |string | initC 容器名称
spec.initContainers[].image |string | initC 镜像
spec.initContainers[].command[] |list | initC 命令
