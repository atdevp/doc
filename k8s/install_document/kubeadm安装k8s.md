<!-- TOC -->

- [使用kubeadm 安装k8s非高可用版本](#%e4%bd%bf%e7%94%a8kubeadm-%e5%ae%89%e8%a3%85k8s%e9%9d%9e%e9%ab%98%e5%8f%af%e7%94%a8%e7%89%88%e6%9c%ac)
  - [安装](#%e5%ae%89%e8%a3%85)
    - [部署规划<allnode>](#%e9%83%a8%e7%bd%b2%e8%a7%84%e5%88%92allnode)
    - [环境初始化<allnode>](#%e7%8e%af%e5%a2%83%e5%88%9d%e5%a7%8b%e5%8c%96allnode)
    - [配置hosts <allnode>](#%e9%85%8d%e7%bd%aehosts-allnode)
    - [Netfilter配置<allnode>](#netfilter%e9%85%8d%e7%bd%aeallnode)
    - [开启kube-proxy的ipvs代理功能<allnode>](#%e5%bc%80%e5%90%afkube-proxy%e7%9a%84ipvs%e4%bb%a3%e7%90%86%e5%8a%9f%e8%83%bdallnode)
    - [关闭swap<allnode>](#%e5%85%b3%e9%97%adswapallnode)
    - [内核升级<allnode>](#%e5%86%85%e6%a0%b8%e5%8d%87%e7%ba%a7allnode)
    - [安装Docker服务<allnode>](#%e5%ae%89%e8%a3%85docker%e6%9c%8d%e5%8a%a1allnode)
    - [安装k8s套件（kubeadm、kubelet、kubectl）<allnode>](#%e5%ae%89%e8%a3%85k8s%e5%a5%97%e4%bb%b6kubeadmkubeletkubectlallnode)
    - [下载k8s服务依赖的镜像<allnode>](#%e4%b8%8b%e8%bd%bdk8s%e6%9c%8d%e5%8a%a1%e4%be%9d%e8%b5%96%e7%9a%84%e9%95%9c%e5%83%8fallnode)
    - [配置harbor仓库<harbornode>](#%e9%85%8d%e7%bd%aeharbor%e4%bb%93%e5%ba%93harbornode)
    - [为docker服务添加本地仓库<allnode>](#%e4%b8%badocker%e6%9c%8d%e5%8a%a1%e6%b7%bb%e5%8a%a0%e6%9c%ac%e5%9c%b0%e4%bb%93%e5%ba%93allnode)
    - [安装flannel网络组建<allnode>](#%e5%ae%89%e8%a3%85flannel%e7%bd%91%e7%bb%9c%e7%bb%84%e5%bb%baallnode)
    - [master节点初始化<k8smasternode>](#master%e8%8a%82%e7%82%b9%e5%88%9d%e5%a7%8b%e5%8c%96k8smasternode)
    - [配置kubectl连接k8s apiserver的权限<allworker>](#%e9%85%8d%e7%bd%aekubectl%e8%bf%9e%e6%8e%a5k8s-apiserver%e7%9a%84%e6%9d%83%e9%99%90allworker)
    - [worker节点加入集群](#worker%e8%8a%82%e7%82%b9%e5%8a%a0%e5%85%a5%e9%9b%86%e7%be%a4)
    - [集群节点查看](#%e9%9b%86%e7%be%a4%e8%8a%82%e7%82%b9%e6%9f%a5%e7%9c%8b)
  - [测试](#%e6%b5%8b%e8%af%95)
    - [登录harbor仓库测试<任意node>](#%e7%99%bb%e5%bd%95harbor%e4%bb%93%e5%ba%93%e6%b5%8b%e8%af%95%e4%bb%bb%e6%84%8fnode)
    - [镜像推送测试<任意node>](#%e9%95%9c%e5%83%8f%e6%8e%a8%e9%80%81%e6%b5%8b%e8%af%95%e4%bb%bb%e6%84%8fnode)
    - [镜像下载测试<任意node>](#%e9%95%9c%e5%83%8f%e4%b8%8b%e8%bd%bd%e6%b5%8b%e8%af%95%e4%bb%bb%e6%84%8fnode)

<!-- /TOC -->
# 使用kubeadm 安装k8s非高可用版本

## 安装
### 部署规划<allnode>

Role | Hostname | IP 
---  | ---  | ---
manager| k8sMaster | 10.211.55.3
worker| k8sNode1| 10.211.55.4
worker| k8sNode2| 10.211.55.5
worker| harbor | 10.211.55.6

### 环境初始化<allnode>
```
yum install -y vim
systemctl stop firewalld
systemctl disable firewalld
setenforce 0
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
```

### 配置hosts <allnode>
```
cat  /etc/hosts

127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

10.211.55.3  k8sMaster
10.211.55.4  k8sNode1
10.211.55.5  k8sNode2
10.211.55.6  harbor.test.com
```

### Netfilter配置<allnode>
```
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

modprobe br_netfilter
sysctl -p /etc/sysctl.d/k8s.conf
```

### 开启kube-proxy的ipvs代理功能<allnode>
```
cat > /etc/sysconfig/modules/ipvs.modules << EOF
#!/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF

chmod 755 /etc/sysconfig/modules/ipvs.modules && bash /etc/sysconfig/modules/ipvs.modules && lsmod && grep -e ip_vs -e nf_conntrack_ipv4

```

### 关闭swap<allnode>
```
swapoff -a && sed -i.bak '/swap/s/^/#/' /etc/fstab
```

### 内核升级<allnode>
* 为什么要进行内核升级呢？
> 3.10的内核版本会出发k8s的bug

* 查看源内核版本
```
uname  -r
3.10.0-1062.el7.x86_64
```

* 导入内核repo
```
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
yum install https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm -y
```

* 查看该repo中提供的可用内核
```
yum --disablerepo="" --enablerepo="elrepo-kernel" list available

kernel-lt.x86_64                            4.4.218-1.el7.elrepo            elrepo-kernel
kernel-lt-devel.x86_64                      4.4.218-1.el7.elrepo            elrepo-kernel
kernel-lt-doc.noarch                        4.4.218-1.el7.elrepo            elrepo-kernel
kernel-lt-headers.x86_64                    4.4.218-1.el7.elrepo            elrepo-kernel
kernel-lt-tools.x86_64                      4.4.218-1.el7.elrepo            elrepo-kernel
kernel-lt-tools-libs.x86_64                 4.4.218-1.el7.elrepo            elrepo-kernel
kernel-lt-tools-libs-devel.x86_64           4.4.218-1.el7.elrepo            elrepo-kernel
kernel-ml.x86_64                            5.6.2-1.el7.elrepo              elrepo-kernel
kernel-ml-devel.x86_64                      5.6.2-1.el7.elrepo              elrepo-kernel
kernel-ml-doc.noarch                        5.6.2-1.el7.elrepo              elrepo-kernel
kernel-ml-headers.x86_64                    5.6.2-1.el7.elrepo              elrepo-kernel
kernel-ml-tools.x86_64                      5.6.2-1.el7.elrepo              elrepo-kernel
kernel-ml-tools-libs.x86_64                 5.6.2-1.el7.elrepo              elrepo-kernel
kernel-ml-tools-libs-devel.x86_64           5.6.2-1.el7.elrepo              elrepo-kernel
perf.x86_64                                 5.6.2-1.el7.elrepo              elrepo-kernel
python-perf.x86_64                          5.6.2-1.el7.elrepo              elrepo-kernel
```

* 安装kernel-lt版本
```
yum --enablerepo=elrepo-kernel install kernel-lt -y
grub2-set-default  "CentOS Linux (4.2.218-1.el7.x86_64) 7 (Core)"
reboot
```

### 安装Docker服务<allnode>
* 配置国内阿里docker源仓库
```
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

* 查看可用的docker版本
```
yum list docker-ce --showduplicates | sort -r

docker-ce.x86_64            3:19.03.8-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.8-3.el7                    @docker-ce-stable
docker-ce.x86_64            3:19.03.7-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.6-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.5-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.4-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.3-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.2-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.1-3.el7                    docker-ce-stable
docker-ce.x86_64            3:19.03.0-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.9-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.8-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.7-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.6-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.5-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.4-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.3-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.2-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.1-3.el7                    docker-ce-stable
docker-ce.x86_64            3:18.09.0-3.el7                    docker-ce-stable
docker-ce.x86_64            18.06.3.ce-3.el7                   docker-ce-stable
docker-ce.x86_64            18.06.2.ce-3.el7                   docker-ce-stable
docker-ce.x86_64            18.06.1.ce-3.el7                   docker-ce-stable
docker-ce.x86_64            18.06.0.ce-3.el7                   docker-ce-stable
docker-ce.x86_64            18.03.1.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            18.03.0.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.12.1.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.12.0.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.09.1.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.09.0.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.06.2.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.06.1.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.06.0.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.03.3.ce-1.el7                   docker-ce-stable
docker-ce.x86_64            17.03.2.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.03.1.ce-1.el7.centos            docker-ce-stable
docker-ce.x86_64            17.03.0.ce-1.el7.centos            docker-ce-stable
```

* 开始安装
```
yum  install docker-ce -y

```

* 查看已安装的docker版本
```
docker version
```

* 启动docker并设置开机启动
```
systemctl start docker && systemctl enable docker
```

* 配置docker，增加docker.json配置文件

  - registry-mirrors: 国内从 Docker Hub 拉取镜像有时会遇到困难，此时可以配置镜像加速器。网易云加速器 https://hub-mirror.c.163.com。 阿里云加速器(需登录账号获取)
  - 
```
mkdir /etc/docker

cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://6oan1qci.mirror.aliyuncs.com", "https://hub-mirror.c.163.com"] 
}
EOF

systemctl daemon-reload &&  systemctl restart docker && systemctl enable docker
```

### 安装k8s套件（kubeadm、kubelet、kubectl）<allnode>
* 配置国内阿里k8s yum源
```
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF


yum clean all && yum makecache
```

* 安装
```
yum install kubeadm kubectl kubelet -y
```

* kubelet 开启启动
```
systemctl enable kubelet
```

### 下载k8s服务依赖的镜像<allnode>
* 下载脚本
```
#!/bin/bash

url="registry.cn-hangzhou.aliyuncs.com/google_containers"
version="1.18.0"
images=(`kubeadm config images list --kubernetes-version=$version | awk -F / '{print $2}'`)
for image in ${images[@]}
do
    docker pull $url/$image
    docker tag $url/$image k8s.gcr.io/$image
    docker rmi -f $url/$image
done
```

### 配置harbor仓库<harbornode>
* 下载地址 https://goharbor.io/docs/1.10/install-config/download-installer/
```
gpg -v –keyserver hkps://keyserver.ubuntu.com –verify harbor-offline-installer-version.tgz.asc
tar xvf harbor-offline-installer-version.tgz
```

* 配置https
```
1、openssl genrsa -out test.com.key 4096

2、openssl req -sha512 -new \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=example/OU=Personal/CN=test.com" \
    -key test.com.key \
    -out test.com.csr

3、cat > v3.ext <<-EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1=test.com
DNS.2=test
DNS.3=harbor
EOF

4、openssl x509 -req -sha512 -days 3650 \
    -extfile v3.ext \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -in test.com.csr \
    -out test.com.crt

5、cp test.com.crt /data/cert/ && cp test.com.key /data/cert/

6、openssl x509 -inform PEM -in test.com.crt -out test.com.cert

7、cp test.com.cert /etc/docker/certs.d/test.com/ &&  cp test.com.key  /etc/docker/certs.d/test.com/ && cp ca.crt        /etc/docker/certs.d/test.com/

```

* 配置harbor.yml
```
hostname: harbor.test.com
certificate: /etc/docker/certs.d/test.com/test.com.cert
private_key: /etc/docker/certs.d/test.com/test.com.key
```

* 安装docker-compose
```
yum install epel-release -y
yum install   python-devel  -y
yum install python-pip -y

yum upgrade python*
pip install --upgrade pip
pip install zipp 
pip install configparser
pip install docker-compose

```

* 启动harbor
```
docker-compose up -d
```

### 为docker服务添加本地仓库<allnode>
```
cat /etc/docker/daemon.json
{
  "registry-mirrors": ["https://6oan1qci.mirror.aliyuncs.com"],
  "exec-opts": ["native.cgroupdriver=systemd"],
  "insecure-registries": ["https://harbor.test.com"]
}

systemctl daemon-reload && systemctl restart docker
```

### 安装flannel网络组建<allnode>
```
wget https://raw.githubusercontent.com/coreos/flannel/2140ac876ef134e0ed5af15c65e414cf26827915/Documentation/kube-flannel.yml
kubectl apply -f kube-flannel.yml
```

### master节点初始化<k8smasternode>
```
cat >kubeadm-config.yaml <<EOF
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
kubernetesVersion: v1.18.0
apiServer:
  certSANs:
  - k8sMaster
  - k8sNode1
  - k8sNode2
  - 10.211.55.3
  - 10.211.55.4
  - 10.211.55.5
networking:
  podSubnet: "10.244.0.0/16"
EOF



kubeadm init --config=kubeadm-config.yaml
```
> 注意如果init失败，可以使用kubeadm reset 重新搞一遍。


### 配置kubectl连接k8s apiserver的权限<allworker>
```
scp k8sMaster:/etc/kubernetes/admin.conf /etc/kubernetes/
echo "export KUBECONFIG=/etc/kubernetes/admin.conf" >> ~/.bash_profile
source .bash_profile
```

### worker节点加入集群

```
kubeadm join 10.211.55.3:6443 --token 4b4qhj.ccdl41ibcizgql85 \
    --discovery-token-ca-cert-hash sha256:de3372e2a2cf2d791febbd20d8d7fb7ee805463584ef353619f10d36292ffb80
```

### 集群节点查看
```
[root@k8sMaster ~]# kubectl   get nodes
NAME        STATUS   ROLES    AGE     VERSION
k8smaster   Ready    master   6h22m   v1.18.0
k8snode1    Ready    <none>   6h9m    v1.18.0
k8snode2    Ready    <none>   6h9m    v1.18.0


[root@k8sMaster ~]# kubectl get po -o wide -n kube-system
NAME                                READY   STATUS    RESTARTS   AGE     IP            NODE        NOMINATED NODE   READINESS GATES
coredns-66bff467f8-cfwpf            1/1     Running   1          6h23m   10.244.0.5    k8smaster   <none>           <none>
coredns-66bff467f8-q6pnm            1/1     Running   2          6h23m   10.244.0.6    k8smaster   <none>           <none>
etcd-k8smaster                      1/1     Running   1          6h23m   10.211.55.3   k8smaster   <none>           <none>
kube-apiserver-k8smaster            1/1     Running   2          6h23m   10.211.55.3   k8smaster   <none>           <none>
kube-controller-manager-k8smaster   1/1     Running   1          6h23m   10.211.55.3   k8smaster   <none>           <none>
kube-flannel-ds-amd64-f4htf         1/1     Running   1          6h18m   10.211.55.3   k8smaster   <none>           <none>
kube-flannel-ds-amd64-fflqx         1/1     Running   1          6h10m   10.211.55.4   k8snode1    <none>           <none>
kube-flannel-ds-amd64-rnx27         1/1     Running   3          6h10m   10.211.55.5   k8snode2    <none>           <none>
kube-proxy-5c9s9                    1/1     Running   5          6h10m   10.211.55.5   k8snode2    <none>           <none>
kube-proxy-b59rw                    1/1     Running   1          6h10m   10.211.55.4   k8snode1    <none>           <none>
kube-proxy-rwlv6                    1/1     Running   1          6h23m   10.211.55.3   k8smaster   <none>           <none>
kube-scheduler-k8smaster            1/1     Running   3          6h23m   10.211.55.3   k8smaster   <none>           <none>

```


## 测试
### 登录harbor仓库测试<任意node>
```
[root@k8sNode2 ~]# docker login https://harbor.test.com
Authenticating with existing credentials...
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

### 镜像推送测试<任意node>
```
docker pull wangyanglinux/myapp:v1
docker tag wangyanglinux/myapp:v1 harbor.test.com/library/myapp:v1
```

### 镜像下载测试<任意node>
* 测试前先删除
```
docker rmi -f wangyanglinux/myapp:v1
docker rmi -f harbor.test.com/library/myapp:v1
```

* 编写pod的资源清单

```
cat > testapp.yaml << EOF
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: default
spec:
 containers:
 - name: myapp
   image: harbor.test.com/library/myapp:v1
EOF
```

* 创建pod
```
kubectl create -f testapp.yaml
```

* 查看
```
[root@k8sNode1 ~]# kubectl  get pod
NAME        READY   STATUS    RESTARTS   AGE
myapp-pod   1/1     Running   0          67m


[root@k8sNode1 ~]# kubectl  get pod -o wide -n default
NAME        READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
myapp-pod   1/1     Running   0          67m   10.244.3.4   k8snode2   <none>           <none>

[root@k8sNode1 ~]# curl 10.244.3.4
Hello MyApp | Version: v1 | <a href="hostname.html">Pod Name</a>
```







