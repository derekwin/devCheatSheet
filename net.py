import os

def createHost(hostname, imagename, mount=None):
    mount = f'-v {os.getcwd()}/hm:/mnt' if mount is None else mount;
    os.system(f'docker run -itd --name {hostname} --net=none --privileged {mount} {imagename}');

def createSwitch(switchname, controller=None, stp=None):
    append = '' if controller is None else f'-- set-controller {switchname} tcp:{controller}' 
    if stp:
        os.system(f'ovs-vsctl add-br {switchname}  -- set bridge {switchname} rstp_enable=true {append}');
        return
    os.system(f'ovs-vsctl add-br {switchname} {append}');

def connectH2S(host, switch, ip=None, gw=None, mac=None, mtu=None):
    ip = '' if ip is None else f'--ipaddress={ip}';
    gw = '' if gw is None else f'--gateway={gw}';
    mac = '' if mac is None else f'--macaddress="{mac}"';
    mtu = '' if mtu is None else f'--mtu=={mtu}';
    os.system(f'ovs-docker add-port {switch} eth0 {host} {ip} {gw} {mac} {mtu}');

def disconnectH2S(host, switch):
    os.system(f'ovs-docker del-port {switch} eth0 {host}');

def connectS2S(switch1, switch2, delay=None, bandwidth=None, tag=None):
    port1 = f'{switch1}-{switch2}';
    port2 = f'{switch2}-{switch1}';
    os.system(f'ip link add {port1} type veth peer name {port2}');
    tag = '' if tag is None else f'-- set port {port1} tag={tag} -- set port {port2} tag={tag}'
    os.system(f'ovs-vsctl add-port {switch1} {port1} -- add-port {switch2} {port2} {tag}');
    os.system(f'ip link set {port1} up');
    os.system(f'ip link set {port2} up');
    option = '' if delay is None else f'delay {delay}';
    option = option if bandwidth is None else f'{option} rate {bandwidth}';
    if option != '':
        os.system(f'tc qdisc replace dev {port1} root netem {option}');
        os.system(f'tc qdisc replace dev {port2} root netem {option}');
    #os.system(f'ovs-vsctl -- add-port {switch1} {port1} -- set interface {port1} type=patch options:peer={port2} -- add-port {switch2} {port2} -- set interface {port2} type=patch options:peer={port1}');

# mbit, kbit
def setQos(switch1, switch2, delay=None, bandwidth=None):
    port1 = f'{switch1}-{switch2}';
    port2 = f'{switch2}-{switch1}';
    option = '' if delay is None else f'delay {delay}';
    option = option if bandwidth is None else f'{option} rate {bandwidth}';
    if option != '':
        os.system(f'tc qdisc replace dev {port1} root netem {option}');
        os.system(f'tc qdisc replace dev {port2} root netem {option}');

def clearQos(switch1, switch2):
    port1 = f'{switch1}-{switch2}';
    port2 = f'{switch2}-{switch1}';
    os.system(f'tc qdisc delete dev {port1} root');
    os.system(f'tc qdisc delete dev {port2} root');

def disconnectS2S(switch1, switch2):
    port1 = f'{switch1}-{switch2}';
    port2 = f'{switch2}-{switch1}';
    os.system(f'ip link del {port1}');
    os.system(f'ovs-vsctl del-port {port1} -- del-port {port2}');
    #os.system(f'ovs-vsctl -- del-port {switch1} {port1} -- del-port {switch2} {port2}');

def deleteHost(host):
    os.system(f'docker stop {host}');
    os.system(f'docker rm {host}');

def deleteSwitch(switchname):
    os.system(f'ovs-vsctl del-br {switchname}');

def addLink(hostname1, hostname2, ip1, ip2):
    port1 = hostname1 + '-' + hostname2;
    port2 = hostname2 + '-' + hostname1;
    pid1 = execCmd("docker inspect -f '{{.State.Pid}}' " + hostname1).splitlines()[0];
    pid2 = execCmd("docker inspect -f '{{.State.Pid}}' " + hostname2).splitlines()[0];
    
    ret = os.system('ip link add ' + port1 + ' type veth peer name ' + port2);
    print(ret)
    
    os.system('mkdir -p /var/run/netns');
    os.system('ln -sf /proc/' + pid1 + '/ns/net /var/run/netns/' + pid1);
    os.system('ln -sf /proc/' + pid2 + '/ns/net /var/run/netns/' + pid2);
    
    addPort2Host(pid1, port1, ip1);
    addPort2Host(pid2, port2, ip2);
    
def delLink(hostname1, hostname2):
    port1 = hostname1 + '-' + hostname2;
    pid1 = execCmd("docker inspect -f '{{.State.Pid}}' " + hostname1).splitlines()[0];
    os.system('ip link delete ' + port1);
    os.system('ip netns exec ' + pid1 + ' ip link del ' + port1);

def delNetns():
    os.system('rm -r /var/run/netns')
    
def addPort2Host(pid, port, ip):
    os.system('ip link set ' + port + ' netns ' + pid);
    os.system('ip netns exec ' + pid + ' ip addr add ' + ip + ' dev ' + port);
    os.system('ip netns exec ' + pid + ' ip link set ' + port + ' up');
    
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text
