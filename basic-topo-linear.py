import os
from functools import partial

# mininet imports
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from mininet.node import RemoteController, Host, OVSKernelSwitch, OVSSwitch
from mininet.node import Controller, OVSController, CPULimitedHost, Node, UserSwitch, IVSSwitch
from subprocess import call

def customNetwork():

    OVSSwitch13 = partial(OVSSwitch, protocols='OpenFlow13')

    # http://mininet.org/api/classmininet_1_1net_1_1Mininet.html#adbd564d924ef02f12ef73fae3393da83
    # defining the network
    # build set to false so it doesn't build until called
    # topo defaults to none which is mininmal
    # ipBase is /4 as testing with 4 hosts
    # switch is OVSKernelSwitch, default switch class
    
    # c0 = RemoteController('c0', ip='127.0.0.1', port = 6633)
    # network = Mininet(ipBase='10.0.0.0/4', topo=None, build=False, controller=c0)


    # adding controller
    # ipBase and port gotten from `sudo mn | dump`, the github link says to use 6633 but doc shows error returned -- 6653 from dump
    network = Mininet(ipBase='10.0.0.0/4', topo=None, build=False)
    info('-------Add controller\n-------')
    # default transport port was 6633 pre-openflow 1.3.2, 6653 post
    c0 = network.addController('c0', controller = RemoteController, ip = '127.0.0.1', port = 6633, protocol = 'tcp')

    # adding switches
    info('-------Add the switches\n-------')
    s1 = network.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = network.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = network.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = network.addSwitch('s4', cls=OVSKernelSwitch)

    # adding hosts
    info('-------Add the hosts\n-------')
    h1 = network.addHost('h1', cls=Host, ip = '10.0.0.1', defaultRoute = None)
    h2 = network.addHost('h2', cls=Host, ip = '10.0.0.2', defaultRoute = None)
    h3 = network.addHost('h3', cls=Host, ip = '10.0.0.3', defaultRoute = None)
    h4 = network.addHost('h4', cls=Host, ip = '10.0.0.4', defaultRoute = None)
    # h1 = network.addHost('h1', cls=Host, ip = '127.0.0.1', defaultRoute = None)
    # h2 = network.addHost('h2', cls=Host, ip = '127.0.0.2', defaultRoute = None)
    # h3 = network.addHost('h3', cls=Host, ip = '127.0.0.3', defaultRoute = None)
    # h4 = network.addHost('h4', cls=Host, ip = '127.0.0.4', defaultRoute = None)

    # links for the network
    info('-------Add the links\n-------')
    network.addLink(h1,s1)
    network.addLink(h2,s2)
    network.addLink(h3,s3)
    network.addLink(h4,s4)
    # interswitch links
    network.addLink(s1,s2)
    network.addLink(s2,s3)
    network.addLink(s3,s4)
    # network.addLink(s2,s4)
    # network.addLink(s3,s4)

    info('-------NETWORK STARTUP\n-------')
    network.build()
    info('-------BOOTING CONTROLLER\n-------')
    for controller in network.controllers:
        controller.start()
    
    # info('-------SWITCH STARTUP CONNECT TO CONTROLLER\n-------')
    # network.get('s1').start([c0])
    # network.get('s2').start([c0])
    # network.get('s3').start([c0])
    # network.get('s4').start([c0])
    info('-------SWITCH STARTUP CONNECT TO CONTROLLER\n-------')
    s1.start([c0])
    s2.start([c0])
    s3.start([c0])
    s4.start([c0])
    
    info('-------Configure switches and hosts\n-------')
    CLI(network)
    network.stop()

if __name__ == '__main__':
    setLogLevel('info')
    customNetwork()