# Morphing Network Slices
# What it does?
From a topology as a star topology you can choose a set of hosts to put in a linear sliced network.
# How it works?
This code works on writing in the switches the rules (thanks to Rest API of Ryu) for the packets inside the sliced network and outside.
# How to run it:
1. To be sure mininet have no network setup yet -> code(sudo mn -c)
2. Run our topology code(sudo python network.py)
