# kvm操作

创建虚拟机

生成iso

`genisoimage -output config.iso -volid cidata -joliet -rock meta-data network-config user-data`

生成qumu硬盘

`qemu-img create -f qcow2 -F qcow2 -o backing_file=/home/ns2022/images/focal-server-cloudimg-amd64.img disk.qcow2 300G`

生成虚拟机

`virt-install --virt-type kvm --network bridge:br0,model=virtio --name vm1 --ram=2048 --vcpus=2 --disk path=/home/ns2022/instances/vm1/disk.qcow2,device=disk,bus=virtio,format=qcow2 --disk /home/ns2022/instances/vm1/config.iso,device=cdrom --os-variant=ubuntu20.04 --graphics vnc,listen=0.0.0.0 --noautoconsole --import`

删除虚拟机

`virsh destroy vm1`

`virsh undefine vm1`


