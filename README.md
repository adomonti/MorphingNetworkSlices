# Morphing Network Slices
## Prerequisites
* [Ryu](https://ryu-sdn.org/)
* Mininet
* Python & Python3
  * Python3 os
  * Python3 time
  * Python3 requests
  * Python mininet.topo
  * Python mininet.net
  * Python mininet.log
  * Python mininet.cli
  * Python mininet.node
## What it does?
From a fixed startopology you can choose a set of hosts to put in a linear sliced network and the remaining hosts will be kept in the star topology.
## How it works?
This code works on writing in the switches the rules (thanks to Rest API of Ryu) for the packets inside the sliced network and outside.
## How to run it:
1. Make sure mininet has no network setup yet -> `sudo mn -c`
2. Run our topology `sudo python network.py`
3. Run Ryu controller with rest api `ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest`
4. Run our app `python3 test_morphing.py` and follow the instruction printed on the screen (look the topology and choose hosts to put in linear slice)
## Our topology
![alt text](https://github.com/adomonti/MorphingNetworkSlices/blob/main/topology.png)
