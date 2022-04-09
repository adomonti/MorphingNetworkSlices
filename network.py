from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController

class RoutingTopo(Topo):
    def build(self):
        switchlist=[]
        hostlist=[]
        for i in range(19):
            switchlist.append(self.addSwitch("s"+str(i+1)))
        
        hostlist.append(self.addHost("h1",mac="00:00:00:00:00:01",ip="192.168.1.1"))
        hostlist.append(self.addHost("h2",mac="00:00:00:00:00:02",ip="192.168.1.2"))
        hostlist.append(self.addHost("h3",mac="00:00:00:00:00:03",ip="192.168.1.3"))
        hostlist.append(self.addHost("h4",mac="00:00:00:00:00:04",ip="192.168.1.4"))
        hostlist.append(self.addHost("h5",mac="00:00:00:00:00:05",ip="192.168.1.5"))
        hostlist.append(self.addHost("h6",mac="00:00:00:00:00:06",ip="192.168.1.6"))
        hostlist.append(self.addHost("h7",mac="00:00:00:00:00:07",ip="192.168.1.7"))
        hostlist.append(self.addHost("h8",mac="00:00:00:00:00:08",ip="192.168.1.8"))
        hostlist.append(self.addHost("h9",mac="00:00:00:00:00:09",ip="192.168.1.9"))
        hostlist.append(self.addHost("h10",mac="00:00:00:00:00:0A",ip="192.168.1.10"))
        hostlist.append(self.addHost("h11",mac="00:00:00:00:00:0B",ip="192.168.1.11"))
        hostlist.append(self.addHost("h12",mac="00:00:00:00:00:0C",ip="192.168.1.12"))


        self.addLink(switchlist[0],switchlist[1],1,1)
        self.addLink(switchlist[0],switchlist[2],2,1)
        self.addLink(switchlist[0],switchlist[3],3,1)
        self.addLink(switchlist[0],switchlist[4],4,1)
        self.addLink(switchlist[0],switchlist[5],5,1)
        self.addLink(switchlist[0],switchlist[6],6,1)

        self.addLink(switchlist[1],switchlist[7],2,1)
        self.addLink(switchlist[1],switchlist[8],3,1)
        
        self.addLink(switchlist[2],switchlist[9],2,1)
        self.addLink(switchlist[2],switchlist[10],3,1)

        self.addLink(switchlist[3],switchlist[11],2,1)
        self.addLink(switchlist[3],switchlist[12],3,1)

        self.addLink(switchlist[4],switchlist[13],2,1)
        self.addLink(switchlist[4],switchlist[14],3,1)

        self.addLink(switchlist[5],switchlist[15],2,1)
        self.addLink(switchlist[5],switchlist[16],3,1)

        self.addLink(switchlist[6],switchlist[17],2,1)
        self.addLink(switchlist[6],switchlist[18],3,1)

        self.addLink(switchlist[7],hostlist[0],2,1)
        self.addLink(switchlist[8],hostlist[1],2,1)
        self.addLink(switchlist[9],hostlist[2],2,1)
        self.addLink(switchlist[10],hostlist[3],2,1)
        self.addLink(switchlist[11],hostlist[4],2,1)
        self.addLink(switchlist[12],hostlist[5],2,1)
        self.addLink(switchlist[13],hostlist[6],2,1)
        self.addLink(switchlist[14],hostlist[7],2,1)
        self.addLink(switchlist[15],hostlist[8],2,1)
        self.addLink(switchlist[16],hostlist[9],2,1)
        self.addLink(switchlist[17],hostlist[10],2,1)
        self.addLink(switchlist[18],hostlist[11],2,1)
        
        
        
        
        
        

if __name__ == '__main__':
    setLogLevel('info')
    topo = RoutingTopo()
    c1 = RemoteController('c1', ip='127.0.0.1')
    net = Mininet(topo=topo, controller=c1)
    net.start()
    hostlist=[]
    for i in range(12):
        hostlist.append(net.get("h"+str(i+1)))
    
    for i in range(12):
        for j in range(12):
            if i!=j:
                hostlist[i].cmd("arp -s 192.168.1."+str(j+1)+" 00:00:00:00:00:"+"{:02x}".format(j+1))
    CLI(net)
    net.stop()
