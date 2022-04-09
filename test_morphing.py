import os
import time
import requests


import os
import time

########### SUPPORT CLASSES ###########

class Host:
    def __init__(self, name, mac):
        self.name = name
        self.mac = mac
    
    def getName(self):
        return self.name
    
    def getMAC(self):
        return self.mac

class Switch:
    def __init__(self, name, nports):
        self.name=name
        self.ports=[]
        for i in range(nports):
            self.ports.append(None)
    
    def getName(self):
        return self.name

    def getConnection(self, port):
        return self.ports[port-1]

    def setConnection(self, port, node):
        self.ports[port-1] = node
    
    def getConnections(self):
        return self.ports

class Network:
    def __init__(self, central_switch):
        self.central_switch = central_switch
        
    def addSwitch(self, switch, parent, parent_port):
        parent.setConnection(parent_port, switch)

    def addHost(self, host, parent, parent_port):
        parent.setConnection(parent_port, host)

    def getSwitch(self, name):
        for x in self.central_switch.getConnections():
            if x is not None and x.getName() == name:
                return x
            for y in x.getConnections():
                if y is not None and y.getName() == name:
                    return y
    
    def getHost(self, name):
        for x in self.central_switch.getConnections():
            if x is not None:
                for y in x.getConnections():
                    if y is not None:
                        for z in y.getConnections():
                            if z is not None and z.name == name:
                                return z
    
    def getParentNode(self, node, level):
        for x in self.central_switch.getConnections():
            if x is node and level==1:
                return self.central_switch
            elif x is not None:
                for y in x.getConnections():
                    if y is node:
                        if level==1:
                            return self.central_switch
                        elif level==2:
                            return x
                    elif y is not None:
                        for z in y.getConnections():
                            if z is node:
                                if level==1:
                                    return self.central_switch
                                elif level==2:
                                    return x
                                elif level==3:
                                    return y

    def getParentPort(self, node, level):
        for i in range(len(self.central_switch.getConnections())):
            x = self.central_switch.getConnections()[i]
            if x is node:
                if level==1:
                    return i+1
                else:
                    return -1
            elif x is not None:
                for j in range(len(x.getConnections())):
                    y = x.getConnections()[j]
                    if y is node:
                        if level == 1:
                            return i+1
                        elif level == 2:
                            return j+1
                        else:
                            return -1
                    elif y is not None:
                        for k in range(len(y.getConnections())):
                            z = y.getConnections()[k]
                            if z is node:
                                if level == 1:
                                    return i+1
                                elif level == 2:
                                    return j+1
                                elif level == 3:
                                    return k+1
                                else:
                                    return -1
    
    def getHosts(self):
        hosts = []
        for x in self.central_switch.getConnections():
            if x is not None:
                for y in x.getConnections():
                    if y is not None:
                        for z in y.getConnections():
                            if z is not None:
                                hosts.append(z)
        return hosts
    

    def printNetwork(self):
        last1=False
        last2=False
        last3=False
        print(self.central_switch.name)
        for i in range(len(self.central_switch.getConnections())):
            x=self.central_switch.getConnections()[i]
            if x is not None:
                if i==len(self.central_switch.getConnections())-1:
                    last1=True
                print(("'" if last1 else "|") + "--> " + x.name)
                for j in range(len(x.getConnections())):
                    y=x.getConnections()[j]
                    if y is not None:
                        if j==len(x.getConnections())-1:
                            last2=True
                        else:
                            last2=False
                        print((" " if last1 else "|") + "      " + ("'" if last2 else "|") + "--> " + y.name)
                        for k in range(len(y.getConnections())):
                            z=y.getConnections()[k]
                            if z is not None:
                                if k==len(y.getConnections())-1:
                                    last3=True
                                else:
                                    last3=False
                                print((" " if last1 else "|") + "      " + (" " if last2 else "|") + "      " + ("'" if last3 else "|") + "--> " + z.name)


def orderHost(elem):
    global net
    i=0
    for x in net.central_switch.getConnections():
            if x is not None:
                i+=1
                for y in x.getConnections():
                    if y is not None:
                        i+=1
                        for z in y.getConnections():
                            if z is not None:
                                i+=1
                                if z.name == elem.getName():
                                    return i

def clear_screen():
    if(os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')

#########################################
########### CONSTRUCT NETWORK ###########
#########################################

## 1st level switch
global net
net = Network(Switch("s1", 6))

## 2nd level switch
net.addSwitch(Switch("s2", 3), net.central_switch, 1)
net.addSwitch(Switch("s3", 3), net.central_switch, 2)
net.addSwitch(Switch("s4", 3), net.central_switch, 3)
net.addSwitch(Switch("s5", 3), net.central_switch, 4)
net.addSwitch(Switch("s6", 3), net.central_switch, 5)
net.addSwitch(Switch("s7", 3), net.central_switch, 6)

## 3rd level switch
net.addSwitch(Switch("s8", 2), net.getSwitch("s2"), 2)
net.addSwitch(Switch("s9", 2), net.getSwitch("s2"), 3)
net.addSwitch(Switch("s10", 2), net.getSwitch("s3"), 2)
net.addSwitch(Switch("s11", 2), net.getSwitch("s3"), 3)
net.addSwitch(Switch("s12", 2), net.getSwitch("s4"), 2)
net.addSwitch(Switch("s13", 2), net.getSwitch("s4"), 3)
net.addSwitch(Switch("s14", 2), net.getSwitch("s5"), 2)
net.addSwitch(Switch("s15", 2), net.getSwitch("s5"), 3)
net.addSwitch(Switch("s16", 2), net.getSwitch("s6"), 2)
net.addSwitch(Switch("s17", 2), net.getSwitch("s6"), 3)
net.addSwitch(Switch("s18", 2), net.getSwitch("s7"), 2)
net.addSwitch(Switch("s19", 2), net.getSwitch("s7"), 3)

## Hosts
net.addHost(Host("h1", "00:00:00:00:00:01"), net.getSwitch("s8"),  2)
net.addHost(Host("h2", "00:00:00:00:00:02"), net.getSwitch("s9"),  2)
net.addHost(Host("h3", "00:00:00:00:00:03"), net.getSwitch("s10"), 2)
net.addHost(Host("h4", "00:00:00:00:00:04"), net.getSwitch("s11"), 2)
net.addHost(Host("h5", "00:00:00:00:00:05"), net.getSwitch("s12"), 2)
net.addHost(Host("h6", "00:00:00:00:00:06"), net.getSwitch("s13"), 2)
net.addHost(Host("h7", "00:00:00:00:00:07"), net.getSwitch("s14"), 2)
net.addHost(Host("h8", "00:00:00:00:00:08"), net.getSwitch("s15"), 2)
net.addHost(Host("h9", "00:00:00:00:00:09"), net.getSwitch("s16"), 2)
net.addHost(Host("h10","00:00:00:00:00:0A"), net.getSwitch("s17"), 2)
net.addHost(Host("h11","00:00:00:00:00:0B"), net.getSwitch("s18"), 2)
net.addHost(Host("h12","00:00:00:00:00:0C"), net.getSwitch("s19"), 2)


clear_screen()
print("Original STAR network:")
net.printNetwork()
time.sleep(1)
print("\n\nPRESS ENTER to continue...")
input()
clear_screen()




#####################################
########### SLICE NETWORK ###########
#####################################

sliced_hosts = []
not_sliced_hosts = net.getHosts()
respup = None

while respup!="":
    print("Select which of these hosts will become part of your slice (type empty string and PRESS ENTER to end the selection): ")
    hosts_available = ""
    for x in net.getHosts():
        if x not in sliced_hosts:
            hosts_available+=x.getName()+" "
    print("Hosts available are:", hosts_available)
    
    resp = input()
    respup = resp.upper()
    if respup != "":
        selected_host = net.getHost(resp)
        if selected_host is not None:
            if selected_host not in sliced_hosts:
                sliced_hosts.append(selected_host)
                not_sliced_hosts.remove(selected_host)
            else:
                print("Host already selected!")
                time.sleep(3)
        else:
            print("Host doesn't exist!")
            time.sleep(3)
    clear_screen()
## Order by port: switches are stateless, so we can treat them like an ordered tree, otherwise we can't create rules: this one because a message
## can go through a switch multiple times (in our case up to 2 times, but the switch can't know if it's the first or second time)
sliced_hosts.sort(key=orderHost)

## Print the new sliced topology
clear_screen()
sliced_topology = ""
for i in range(len(sliced_hosts)):
    sliced_topology+=sliced_hosts[i].getName()
    if i < len(sliced_hosts)-1:
        sliced_topology+="--"
print("The algorithm made a sliced topology defined as follow:",sliced_topology)


#####################################################
########### CONSTRUCT NEW STAR TOPOLOGY #############
#####################################################

##First Level
rules_central_switch_star = []
for host in not_sliced_hosts:
    port = net.getParentPort(host, 1)
    rules_central_switch_star.append((40000,"*",host.getMAC(),"*",[port]))
rules_central_switch_star.append((40000,"*","ff:ff:ff:ff:ff:ff","*",[1,2,3,4,5,6]))

##Second Level
rules_second_level_star = []
switch_one_child = []
switch_two_children = []
for host in not_sliced_hosts:
    node = net.getParentNode(host, 2)
    if node in switch_one_child:
        switch_two_children.append(node)
        switch_one_child.remove(node)
    else:
        switch_one_child.append(node)

for sw in switch_one_child:
    switch_rules=[]
    for host in not_sliced_hosts:
        if net.getParentNode(host, 2) is sw:
            port = net.getParentPort(host, 2)
            switch_rules.append((40000,"*",host.getMAC(),"*",[port]))
    switch_rules.append((40000,"*","ff:ff:ff:ff:ff:ff","*",[1,2]))
    switch_rules.append((30000,"*","*","*",[1]))
    rules_second_level_star.append((sw,switch_rules))

for sw in switch_two_children:
    switch_rules=[]
    for host in not_sliced_hosts:
        if net.getParentNode(host, 2) is sw:
            port = net.getParentPort(host, 2)
            switch_rules.append((40000,"*",host.getMAC(),"*",[port]))
    switch_rules.append((40000,"*","ff:ff:ff:ff:ff:ff","*",[1,2,3]))
    switch_rules.append((30000,"*","*","*",[1]))
    rules_second_level_star.append((sw,switch_rules))

##Third Level
rules_third_level_star = []
for host in not_sliced_hosts:
    switch_rules=[]
    node = net.getParentNode(host, 3)
    for nothost in sliced_hosts:
        switch_rules.append((45000,"*",nothost.getMAC(),"*",[]))
    switch_rules.append((40000,"*","*",1,[2]))
    switch_rules.append((30000,"*","*","*",[1]))
    rules_third_level_star.append((node,switch_rules))


print("\n\n####################### STAR TOPOLOGY SLICE #######################")
print("\n\nRules of 1st level switch:\n\n\t--"+net.central_switch.getName()+"--")
for x in rules_central_switch_star:
    print("\t",x)

print("\n\nRules of 2nd level switches:")
for x in rules_second_level_star:
    print("\n\t--"+x[0].getName()+"--")
    for y in x[1]:
        print("\t", y)

print("\n\nRules of 3rd level switches:")
for x in rules_third_level_star:
    print("\n\t--"+x[0].getName()+"--")
    for y in x[1]:
        print("\t", y)




#####################################################
########### CONSTRUCT NEW SLICED TOPOLOGY ###########
#####################################################



########### 1st LEVEL CENTRAL SWITCH RULES ###########

## Get association first level ports - hosts
first_level_mac_port = []
for x in sliced_hosts:
    port = net.getParentPort(net.getHost(x.getName()), 1)
    first_level_mac_port.append((x.getMAC(), port))


## Construct rules for central switch
rules_central_switch = []

#scroll source
for i_src in range(len(first_level_mac_port)):
    src = first_level_mac_port[i_src]
    #sroll destination
    for i_dst in range(len(first_level_mac_port)):
        dst = first_level_mac_port[i_dst]

        #if destination is to the RIGHT of source
        if i_dst > i_src:
            for i_port in range(i_src,i_dst): #for each in port, forward to the next right Port Of Interest (POI=port that connects switches in the slice)
                in_port = first_level_mac_port[i_port][1]
                out_port = first_level_mac_port[i_port+1][1]
                if out_port != in_port: #only if they're situated in different 2nd-level-switches
                    rules_central_switch.append((50000,src[0],dst[0],in_port,[out_port]))
        
        #if destination is to the LEFT of source
        elif i_dst < i_src:
            for i_port in range(i_src,i_dst,-1): #for each in port, forward to the previous left Port Of Interest
                in_port = first_level_mac_port[i_port][1]
                out_port = first_level_mac_port[i_port-1][1]
                if out_port != in_port: #only if they're situated in different 2nd-level-switches
                    rules_central_switch.append((50000,src[0],dst[0],in_port,[out_port]))
    #broadcast rules
    broadcast_port=[]
    for port in first_level_mac_port:
        if port[1] not in broadcast_port and port[1]!=src[1]:
            broadcast_port.append(port[1])
    rules_central_switch.append((50005,src[0],"ff:ff:ff:ff:ff:ff",src[1],broadcast_port))

print("\n\n\n\n####################### STRING TOPOLOGY SLICE #######################")
print("\n\nRules of 1st level switch:\n\n\t--"+net.central_switch.getName()+"--")
for x in rules_central_switch:
    print("\t",x)

            
########### 2nd LEVEL SWITCH RULES ###########

## Get 2nd level switches of interests
sliced_switches_2nd = []
for x in sliced_hosts:
    node = net.getParentNode(net.getHost(x.getName()), 2)
    if node not in sliced_switches_2nd:
        sliced_switches_2nd.append(node)

## Get association second level ports - hosts
second_level_mac_port = []
for x in sliced_switches_2nd:
    host_connected=[]
    children=""
    for y in sliced_hosts:
        node = net.getParentNode(net.getHost(y.getName()), 2)
        if node is x:
            port = net.getParentPort(net.getHost(y.getName()), 2)
            host_connected.append((y.getMAC(), port))
            if port == 2 and children == "":
                children="L"
            elif port == 3 and children == "":
                children="R"
            elif port!= 1:
                children="B"
        else:
            host_connected.append((y.getMAC(), 1))
    second_level_mac_port.append((x, children, host_connected))

##Construct rules for second level switches
rules_second_level=[]

for sw in second_level_mac_port:

    ##In case of: LEFT ONLY CHILD
    if sw[1]=="L":
        switch_rules=[]
        switch_rules.append((50000,"*","*",2,[1])) #in_port=2
        for host in sw[2]:
            if host[1]==1:
                switch_rules.append((50000,host[0],"*",1,[2])) #in_port=1, src=host_in_slice

        rules_second_level.append((sw[0],switch_rules))

    ##In case of: RIGHT ONLY CHILD
    if sw[1]=="R":
        switch_rules=[]
        switch_rules.append((50000,"*","*",3,[1])) #in_port=3
        for host in sw[2]:
            if host[1]==1:
                switch_rules.append((50000,host[0],"*",1,[3])) #in_port=1, src=host_in_slice

        rules_second_level.append((sw[0],switch_rules))

    ##In case of: BOTH CHILDREN
    if sw[1]=="B":
        switch_rules=[]
        index_host=0
        condition="L"
        for host in sw[2]:
            #from external left hosts
            if condition=="L":
                if host[1]==2:
                    condition="CR"
                else:
                    switch_rules.append((50000,host[0],"*",1,[2]))
                    switch_rules.append((50000,host[0],"*",2,[3]))
                    switch_rules.append((50000,host[0],"*",3,[1]))
                    switch_rules.append((50005,host[0],"ff:ff:ff:ff:ff:ff",1,[2,3]))

            #from internal to right (internal or external) hosts
            if condition=="CR":
                if host[1]==3:
                    condition="CL"
                else:
                    for x in range(index_host+1,len(sw[2])):
                        switch_rules.append((50000,"*",sw[2][x][0],2,[3]))
                        if x!=index_host+1:
                            switch_rules.append((50000,"*",sw[2][x][0],3,[1]))
                    switch_rules.append((50005,"*","ff:ff:ff:ff:ff:ff",2,[1,3]))
            
            #from internal to left (internal or external) hosts
            if condition=="CL":
                if host[1]==1:
                    condition="R"
                else:
                    for x in range(index_host-1,-1,-1):
                        switch_rules.append((50000,"*",sw[2][x][0],3,[2]))
                        if x!=index_host-1:
                            switch_rules.append((50000,"*",sw[2][x][0],2,[1]))
                    switch_rules.append((50005,"*","ff:ff:ff:ff:ff:ff",3,[1,2]))
            
            #from external right hosts
            if condition=="R":
                switch_rules.append((50000,host[0],"*",1,[3]))
                switch_rules.append((50000,host[0],"*",3,[2]))
                switch_rules.append((50000,host[0],"*",2,[1]))
                switch_rules.append((50005,host[0],"ff:ff:ff:ff:ff:ff",1,[2,3]))

            index_host+=1

        rules_second_level.append((sw[0],switch_rules))

print("\n\nRules of 2nd level switches:")
for x in rules_second_level:
    print("\n\t--"+x[0].getName()+"--")
    for y in x[1]:
        print("\t", y)
        
            
########### 3rd LEVEL SWITCH RULES ###########

## Get 3rd level switches of interests and association host-port
third_level_mac_port = []
for x in sliced_hosts:
    node = net.getParentNode(net.getHost(x.getName()), 3)
    host_connected=[]
    for y in sliced_hosts:
        if y is x:
            host_connected.append((y.getMAC(),2))
        else:
            host_connected.append((y.getMAC(),1))
    third_level_mac_port.append((node,host_connected))

## Construct rules for third level switches
rules_third_level=[]
for sw in third_level_mac_port:
    switch_rules=[]
    for host in sw[1]:
        if host[1]==1:
            switch_rules.append((50001,"*",host[0],2,[1]))
        else:
            switch_rules.append((50001,"*",host[0],1,[2]))
    switch_rules.append((50000,"*","*",2,[])) #drop
    switch_rules.append((50000,"*","*",1,[1,2])) #double action: ofpp_in_port and forward
    switch_rules.append((50005,"*","ff:ff:ff:ff:ff:ff",1,[2])) #broadcast
    switch_rules.append((50005,"*","ff:ff:ff:ff:ff:ff",2,[1])) #broadcast
    rules_third_level.append((sw[0],switch_rules))

print("\n\nRules of 3rd level switches:")
for x in rules_third_level:
    print("\n\t--"+x[0].getName()+"--")
    for y in x[1]:
        print("\t", y)


api_url="http://localhost:8080/stats/flowentry/add"
#print("\n")
for i in range(19):
    api="http://localhost:8080/stats/flowentry/clear/"+str(i+1)
    response = requests.delete(api) #delete all entry for every switch

    my_json={}
    my_json["dpid"]=(i+1)
    my_json["priority"]=2
    my_json["match"]={}
    my_json["action"]=[]
    response = requests.post(api_url,json=my_json)
    
print("\n\nRules for line topology:\n\n")

for x in rules_central_switch:  #add rules for the central switch (rules for line topology slice)
    my_json={}
    my_json["dpid"]=int(net.central_switch.getName()[1])
    my_json["priority"]=x[0]
    my_match={"in_port":x[3]}
    if x[1]!="*":
        my_match["eth_src"]=x[1]
    if x[2]!="*":
        my_match["eth_dst"]=x[2]
    my_json["match"]=my_match
    if x[4]!=[]:
        temp=[]
        for i in x[4]:
            if x[3]!=i:
                temp.append({"type":"OUTPUT","port":i})
            else:
                temp.append({"type":"OUTPUT","port":"OFPP_IN_PORT"})
        my_json["actions"]=temp
    else:
        my_json["actions"]=[]    
    response=requests.post(api_url,json=my_json)
    print(my_json)
    print(response)
    print("\n")
print("\n\n\n\n")

for x in rules_second_level:    #add rules for the second level switches (rules for line topology slice)
    my_json={}
    my_json["dpid"]=int(x[0].getName()[x[0].getName().find("s")+1:])
    for y in x[1]:
        my_json["priority"]=y[0]
        my_match={"in_port":y[3]}
        if y[1]!="*":
            my_match["eth_src"]=y[1]
        if y[2]!="*":
            my_match["eth_dst"]=y[2]
        my_json["match"]=my_match
        temp=[]
        if y[4]!=[]:
            for i in y[4]:
                if y[3]!=i:
                    temp.append({"type":"OUTPUT","port":i})
                else:
                    temp.append({"type":"OUTPUT","port":"OFPP_IN_PORT"})
            my_json["actions"]=temp
        else:
            my_json["actions"]=[]    
        response=requests.post(api_url,json=my_json)
        print(my_json)
        print(response)
        print("\n")
    print("\n\n\n\n")

for x in rules_third_level: #add rules for the third level switches (rules for line topology slice)
    my_json={}
    my_json["dpid"]=int(x[0].getName()[x[0].getName().find("s")+1:])
    for y in x[1]:
        my_json["priority"]=y[0]
        my_match={"in_port":y[3]}
        if y[1]!="*":
            my_match["eth_src"]=y[1]
        if y[2]!="*":
            my_match["eth_dst"]=y[2]
        my_json["match"]=my_match
        temp=[]
        if y[4]!=[]:
            for i in y[4]:
                if y[3]!=i:
                    temp.append({"type":"OUTPUT","port":i})
                else:
                    temp.append({"type":"OUTPUT","port":"OFPP_IN_PORT"})

            my_json["actions"]=temp
        else:
            my_json["actions"]=[]    
        response=requests.post(api_url,json=my_json)
        print(my_json)
        print(response)
        print("\n")
    print("\n\n\n\n")

print("Rules for star topology:\n\n")
for x in rules_central_switch_star:  #add rules for the central switch (rules for star topology slice)
    my_json={}
    my_json["dpid"]=int(net.central_switch.getName()[1])
    my_json["priority"]=x[0]
    my_match={}
    if x[3]!="*":
        my_match={"in_port":x[3]}
    if x[1]!="*":
        my_match["eth_src"]=x[1]
    if x[2]!="*":
        my_match["eth_dst"]=x[2]
    my_json["match"]=my_match
    if x[4]!=[]:
        temp=[]
        for i in x[4]:
            temp.append({"type":"OUTPUT","port":i})
        my_json["actions"]=temp
    else:
        my_json["actions"]=[]    
    response=requests.post(api_url,json=my_json)
    print(my_json)
    print(response)
    print("\n")
print("\n\n\n\n")

for x in rules_second_level_star:   #add rules for the second level switches (rules for star topology slice)
    my_json={}
    my_json["dpid"]=int(x[0].getName()[x[0].getName().find("s")+1:])
    for y in x[1]:
        my_json["priority"]=y[0]
        my_match={}
        if y[3]!="*":
            my_match={"in_port":y[3]}
        if y[1]!="*":
            my_match["eth_src"]=y[1]
        if y[2]!="*":
            my_match["eth_dst"]=y[2]
        my_json["match"]=my_match
        temp=[]
        if y[4]!=[]:
            for i in y[4]:
                temp.append({"type":"OUTPUT","port":i})
            my_json["actions"]=temp
        else:
            my_json["actions"]=[]    
        response=requests.post(api_url,json=my_json)
        print(my_json)
        print(response)
        print("\n")
    print("\n\n\n\n")

for x in rules_third_level_star:    #add rules for the third level switch (rules for star topology slice)
    my_json={}
    my_json["dpid"]=int(x[0].getName()[x[0].getName().find("s")+1:])
    for y in x[1]:
        my_json["priority"]=y[0]
        my_match={"in_port":y[3]}
        my_match={}
        if y[3]!="*":
            my_match={"in_port":y[3]}
        
        if y[1]!="*":
            my_match["eth_src"]=y[1]
        if y[2]!="*":
            my_match["eth_dst"]=y[2]
        my_json["match"]=my_match
        temp=[]
        if y[4]!=[]:
            for i in y[4]:
                if y[3]!=i:
                    temp.append({"type":"OUTPUT","port":i})
                else:
                    temp.append({"type":"OUTPUT","port":"OFPP_IN_PORT"})
            my_json["actions"]=temp
            """response=requests.post(api_url,json=my_json)
            print(my_json)
            print("Response code",response)"""
        else:
            my_json["actions"]=[]    
        response=requests.post(api_url,json=my_json)
        print(my_json)
        print(response)
        print("\n")
    print("\n\n\n\n")
