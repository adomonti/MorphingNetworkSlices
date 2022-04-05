# Morphing Network Slices
# Prerequisites
* Ryu
* Mininet
* Python & Python3
* * adad
# What it does?
From a topology as a star topology you can choose a set of hosts to put in a linear sliced network.
# How it works?
This code works on writing in the switches the rules (thanks to Rest API of Ryu) for the packets inside the sliced network and outside.
# How to run it:
1. To be sure mininet have no network setup yet -> `sudo mn -c`
2. Run our topology `sudo python network.py`
3. Run Ryu controller with rest api `ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest`
4. Run our app `python3 test_morphing.py`
