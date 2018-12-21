"""
Author: Sean Kennedy (seankennedy@ieee.org)
"""
from scapy.all import *
from random import randint
import pandas as pd


packet_path = 'how_many_days_untill_christmas_5_30s.pcap'

# Load packets in as type: scapy packet_list
packets = rdpcap(packet_path)

# How many packets in the pcap file?
print("Packets in pcap file: {}".format(len(packets)))

# Alright lets pick a random packet and take a deeper look
packet_no = randint(0, len(packets) - 1)
packet = packets[packet_no]

# What does a packet look like now?
print("Content of packet {} is {}".format(packet_no, packets[packet_no]))
# Okay it appears to be a list of bytes

# And the type?
print("The type of the packet is {}".format(type(packet)))
# The type is <class 'scapy.layers.l2.Ether'>, ok... what can we do with that?

# Ok, now lets see a list of methods for this class
print("Instance methods in the {} class include: {}".format(type(packet), dir(packet)))

# After looking through the list of methods lets try some out...

print(packet.display())
# print(packet.fields_desc)
# print(packet.len)

# Loop through all of the packets in the pcap and print the size in bytes

# for p in packets:
    # print(p.len)

# Let's create a dataframe to store our results
echo_df = pd.DataFrame(columns=['time', 'size', 'src', 'dst', 'protocol'])
echo_src_df = pd.DataFrame(columns=['time', 'size'])
echo_dst_df = pd.DataFrame(columns=['time', 'size'])

# Keep track of our Echo's IP Address
echo_ip = '192.168.86.40'
init_time = packet[0].time
print(init_time)

# Just the packets from the echo
print("========IP SOURCE IS ECHO========")
for p in packets:
    if p[IP].src == echo_ip:
        print("Time: {} Size: {}".format(p[IP].time, p.len))

# Now the packets destined for the Echo
print("========IP DESTINATION IS ECHO========")
for p in packets:
    if p[IP].dst == echo_ip:
        print("Time: {} Size: {}".format(p[IP].time, p.len))

# Create 3 dataframes: 1 src, 1 dst, and 1 all
for p in packets:
    if p[IP].src == echo_ip or p[IP].dst == echo_ip:
        echo_df.loc[-1] = [p[IP].time, p.len, p[IP].src, p[IP].dst, p[IP].proto]
        echo_df.index = echo_df.index + 1
        echo_df = echo_df.sort_index()
    if p[IP].src == echo_ip:
        echo_src_df.loc[-1] = [p[IP].time, p.len]
        echo_src_df.index = echo_src_df.index + 1
        echo_src_df = echo_src_df.sort_index()
    if p[IP].dst == echo_ip:
        echo_dst_df.loc[-1] = [p[IP].time, p.len]
        echo_dst_df.index = echo_dst_df.index + 1
        echo_dst_df = echo_dst_df.sort_index()

print(echo_df.head(10))

# Ok now lets save the data to a csv to make it easier to work with later
echo_df.to_csv('echo_df.csv')

