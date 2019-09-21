### Author:: Anupriya

import sys

class Node:
    def __init__(self, bit, traffic):
        self.bit = bit
        self.traffic = traffic
        self.left = None
        self.right = None
        self.parent = None
    
    def add_traffic(self, extra_traffic):
        self.traffic += extra_traffic

class IP_Binary_Tree:
    def __init__(self, filename):
        self.root = Node('-1', 0)
        self.filename = filename
        self.traffic_to_subnet = {}
    
    def insert_file_data(self):
        with open(self.filename) as file:
            for line in file:
                ip,traffic = line.split(' ')
                traffic = int(traffic.strip('\n'))
                
                self.root.traffic += traffic
                
                bits = self.convert_ip_to_bit_string(ip)
                self.insert_ip_traffic(self.root, bits, 0, traffic)
               
    def insert_ip_traffic(self, subroot, ip_bits, index, traffic):
        if len(ip_bits) == index:
            return
        
        if ip_bits[index] == '0':
            if subroot.left == None:
                subroot.left = Node(ip_bits[index], traffic)
                subroot.left.parent = subroot
            else:
                subroot.left.traffic += traffic
            self.insert_ip_traffic(subroot.left, ip_bits, index+1, traffic)
        else:
            if subroot.right == None:
                subroot.right = Node(ip_bits[index], traffic)
            else:
                subroot.right.traffic += traffic
                subroot.right.parent = subroot
            self.insert_ip_traffic(subroot.right, ip_bits, index+1, traffic)
    
    def get_largest_cidrs(self, thres):
        thres = (self.root.traffic * thres)//100
        self.get_largest_cidrs_helper(self.root.left, thres)
        self.get_largest_cidrs_helper(self.root.right, thres)
        
    def get_largest_cidrs_helper(self, subroot, thres):
        if subroot == None:
            return
        if self.traffic_is_thres(subroot, thres):
            subnet = self.get_subnet(subroot)
            subnet = self.convert_bit_string_to_ip(subnet)
            if subroot.traffic not in self.traffic_to_subnet:
                self.traffic_to_subnet[subroot.traffic] = []
            self.traffic_to_subnet[subroot.traffic].append(subnet)
            
        self.get_largest_cidrs_helper(subroot.left, thres)
        self.get_largest_cidrs_helper(subroot.right, thres)
        
    def get_subnet(self, subroot):
        if subroot.bit == '-1':
            return ""
        return self.get_subnet(subroot.parent) + subroot.bit
    
    def traffic_is_thres(self, subroot, thres):
        if subroot.traffic >= thres and subroot.left != None and subroot.right != None and \
            (subroot.left.traffic < thres and subroot.right.traffic < thres):
                return True
        return False
                                    
    def convert_ip_to_bit_string(self, ip):
        bytes = ip.split('.')
        
        bit_string = ""
        for byte in bytes:
            bit_string += f'{int(byte):08b}'
        return bit_string
    
    def convert_bit_string_to_ip(self, subnet):
        subnet_bits = len(subnet)
        cidr = subnet + ('0'*subnet_bits)
        
        return str(int(cidr[0:8], 2)) + '.' + str(int(cidr[8:16], 2)) + '.' +\
                str(int(cidr[16:24], 2)) + '.' + str(int(cidr[24:32], 2)) + '/'+ str(subnet_bits)
    
    def print_subnets(self):
        for traffic in sorted(self.traffic_to_subnet, reverse = True):
            for ip in sorted(self.traffic_to_subnet[traffic]):
                print(ip + ' ' + str(traffic))
    
if __name__ == "__main__":
    ip_tree = IP_Binary_Tree(sys.argv[1])
    ip_tree.insert_file_data()
    ip_tree.get_largest_cidrs(int(sys.argv[2]))
    ip_tree.print_subnets()
        
        
            
            
            
        
        
