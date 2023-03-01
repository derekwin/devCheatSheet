# 常用的网络设置

netplan设置网络

`sudo vim /etc/netplan/50-cloud-init.yaml`

```
enp6s0:
    addresses:
    - 10.0.0.1/24
    dhcp4: false
    gateway4: 10.0.0.0
    nameservers:
        addresses:
        - 114.114.114.114
        - 8.8.8.8
```

应用配置

`sudo netplan apply`


端口映射

`sudo iptables -t nat -A PREROUTING -p tcp --dport 18000 -j DNAT --to 10.12.0.101:8000`

`sudo iptables -L -t nat`


查看端口开放情况

`netstat -npl`