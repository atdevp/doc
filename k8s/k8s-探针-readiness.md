## k8s容器探针

### 探针
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

### readiness
> 称之为就绪检测，检测容器是否准备好提供服务。如果配置了检测，则默认是failed。如果没有配置默认为success。

### readiness-HTTPGetAction
- readiness-httpget.yaml
```
apiVersion: v1
kind: Pod
metadata:
  name: readiness-httpget-pod
  namespace: default

spec:
  containers:
  - name: readiness-httpget-c1
    image: harbor.test.com/library/myapp:v1
    imagePullPolicy: IfNotPresent
    ports:
    - name: http
      containerPort: 80
    readinessProbe:
      httpGet:
        port: http
        path: /index1.html
      initialDelaySeconds: 2
      periodSeconds: 3
```

- 状态

```
[root@k8sNode1 ~]# kubectl   get pod
NAME                    READY   STATUS    RESTARTS   AGE
readiness-httpget-pod   0/1     Running   0          3s

```

- 日志

```
[root@k8sNode1 ~]# kubectl  describe pod readiness-httpget-pod

Warning  Unhealthy  <invalid> (x4 over 0s)  kubelet, k8snode2  Readiness probe failed: HTTP probe failed with statuscode: 404
```

```
[root@k8sNode1 ~]# kubectl exec   readiness-httpget-pod -c readiness-httpget-c1 -it /bin/sh
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl kubectl exec [POD] -- [COMMAND] instead.
/ # cd /usr/share/nginx/html
/usr/share/nginx/html # echo "hello world" >>index1.html
/usr/share/nginx/html # exit
[root@k8sNode1 ~]# kubectl  get pod
NAME                    READY   STATUS    RESTARTS   AGE
readiness-httpget-pod   1/1     Running   0          2m8s
```

### readiness-ExecAction
- readiness-exec.yaml
```
apiVersion: v1
kind: Pod
metadata:
  name: readiness-exec-pod
  namespace: default

spec:
  containers:
  - name: readiness-exec-c1
    image: harbor.test.com/library/myapp:v1
    imagePullPolicy: IfNotPresent
    readinessProbe:
      exec:
        command: ["test", "-e", "/usr/share/nginx/html/index1.html"]
      initialDelaySeconds: 2
      periodSeconds: 3
```

- 状态

```
[root@k8sNode1 ~]# kubectl   apply -f readiness-exec.yaml
pod/readiness-exec-pod created
[root@k8sNode1 ~]# kubectl  get pods
NAME                 READY   STATUS    RESTARTS   AGE
readiness-exec-pod   0/1     Running   0          4s
[root@k8sNode1 ~]# kubectl  get pods
NAME                 READY   STATUS    RESTARTS   AGE
readiness-exec-pod   0/1     Running   0          8s
```

- 日志

```
[root@k8sNode1 ~]# kubectl  describe pod  readiness-exec-pod

Warning  Unhealthy  78s (x22 over 2m21s)  kubelet, k8snode1  Readiness probe failed:
```

```
[root@k8sNode1 ~]# kubectl exec readiness-exec-pod -c readiness-exec-c1 -it /bin/sh
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl kubectl exec [POD] -- [COMMAND] instead.
/ # echo "hello k8s" >/usr/share/nginx/html/index1.html
/ # exit
[root@k8sNode1 ~]# kubectl  get pods
NAME                 READY   STATUS    RESTARTS   AGE
readiness-exec-pod   1/1     Running   0          3m33s
```

### readiness-TCPSocketAction
- readiness-exec.yaml
```
apiVersion: v1
kind: Pod
metadata:
  name: readiness-tcp-pod
  namespace: default

spec:
  containers:
  - name: readiness-tcp-c1
    image: harbor.test.com/library/myapp:v1
    imagePullPolicy: IfNotPresent
    readinessProbe:
      tcpSocket:
        port: 80
      timeoutSeconds: 1
      initialDelaySeconds: 2
      periodSeconds: 3
```

- 状态

```
[root@k8sNode1 ~]# kubectl apply -f readiness-tcp.yaml
pod/readiness-tcp-pod created
[root@k8sNode1 ~]# kubectl  get pod
NAME                READY   STATUS    RESTARTS   AGE
readiness-tcp-pod   0/1     Running   0          4s
[root@k8sNode1 ~]# kubectl  get pod
NAME                READY   STATUS    RESTARTS   AGE
readiness-tcp-pod   1/1     Running   0          5s
[root@k8sNode1 ~]# kubectl  get pod
NAME                READY   STATUS    RESTARTS   AGE
readiness-tcp-pod   1/1     Running   0          6s
```


