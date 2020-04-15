## k8s容器探针

## 探针
> 探针是kubelet执行，有三种Handler。

* ExecAction
> 容器内部执行命令，成功返回0，则认为本次诊断ok，反之不ok。

* TCPSocketAction
> 端口检测，端口通，则认为本次诊断ok，反之不ok。

* HTTPGetAction
> 对容器IP发送http的get请求，如果状态码满足400>code>=200，认为本次诊断ok，反之不ok。

### 探测结果
* success
* failed
* unkown 诊断失败，不采取措施


### liveness
> 称之为持续检测，检测容器运行过程中提供检测。

### 