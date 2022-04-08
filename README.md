# Morphing Network Slices
## Prerequisites
* Linux OS (tested on [Ubuntu 20.04](https://releases.ubuntu.com/20.04/))
* [Ryu](https://ryu-sdn.org/)
* [Mininet](http://mininet.org/)
* [Python & Python3](https://www.python.org/)
  * Python3 os
  * Python3 time
  * Python3 requests
  * Python mininet.topo
  * Python mininet.net
  * Python mininet.log
  * Python mininet.cli
  * Python mininet.node
## Description
Project done with collaboration of University of Trento (DISI department) for the exam of "Softwarized and Virtualized Mobile Networks".
From a fixed star topology you can choose a set of hosts to put in a sliced linear topology network and the remaining hosts will be put in the sliced star topology network.
This code works on writing in the switches the rules (thanks to Rest API of Ryu) for the packets inside the sliced network and outside.
## Visuals
The **physical network** before the slicing (standard ethernet star topology):

![alt text](https://github.com/adomonti/MorphingNetworkSlices/blob/main/images/topology.png)

The network after the slicing (it's been **divided in 2 slice**):

![alt text](https://github.com/adomonti/MorphingNetworkSlices/blob/main/images/topology%20sliced.png)

Focus on **linear topology** slice:

![alt text](https://github.com/adomonti/MorphingNetworkSlices/blob/main/images/linear%20topology.png)

Focus on **star topology** slice:

![alt text](https://github.com/adomonti/MorphingNetworkSlices/blob/main/images/star%20topology.png)
## Installation
You have to install all the prerequisites above. Then you can easily install our application by simply downloading this repository with command:
```
git clone https://github.com/adomonti/MorphingNetworkSlices.git
```
## Usage
1. Position in your workspace directory (where you downloaded files, eg. home directory ~/)
1. Make sure mininet has no network setup yet -> `sudo mn -c`
2. Run our topology `sudo python network.py`
3. Run Ryu controller with rest api `ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest`
4. Run our app `python3 test_morphing.py` and follow the instruction printed on the screen (look at topology and choose hosts to put in linear slice)
## Authors
[adomonti](https://github.com/adomonti)

[jvj00](https://github.com/jvj00)

[TheVSNA](https://github.com/TheVSNA)
