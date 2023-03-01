# 将kvm虚拟机与ovs虚拟机相连

创建ovs虚拟交换机(create ovs switch by net.py)

`net.create()`

连接ovs

`net.connectS2S("s1", "s2", "200ms", "10Mbps")`

`net.setQos("s1", "s2", "10ms", "200Mbps")`  // 修改链路参数

连接

`virsh attach-interface vm1(虚拟机名) --type bridge --source s1(ocs交换机) --model virtio --config`

连接后还无法使用，需要进一步进行设置

`virsh edit vm1`   // 修改配置

在增加的网桥内增加下面字段

`<virtualport type='openvswitch'/>`

保存退出后，会自动生成配置


查看网桥信息

`ip -a`

查看虚拟机的网桥信息

`virsh domiflist vm1`

解绑连接

`virsh detach-interface vm1 --type bridge --mac 52:54:00:d3:e5:d4(对应虚拟网桥的mac)`

**所有操作均需关闭虚拟机并重启才会生效**