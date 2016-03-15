#!/usr/bin/python -u
import sys
import socket
import select
from time import time
import json


class Bridge(object):
    # the constructor of the bridge
    def __init__(self, id, lans):
        self.id = id
        self.lans = lans
        self.forwarding_table = {}
        self.bridge_table = {}
        self.parent = {}
        self.ignored_ports = []
        self.sockets = []
        self.bpdu_time = 0

    # pads the name with null bytes at the end
    def pad(self, name):
        result = '\0' + name
        while len(result) < 108:
            result += '\0'
        return result

    # connect sockets to each lan
    def sock(self):
        for x in range(len(LAN)):
            s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            s.connect(self.pad(LAN[x]))
            self.sockets.append(s)
            self.ignored_ports.append(1)

    # update the bridge table
    def change_bridge_table(self, id, port, root, cost):
        self.bridge_table[id] = {'src': port, 'root': root, 'cost': cost,
                                 'time': time() * 1000 + 750}

    # broadcast the bpdu message
    def broadcast_bpdu(self):
        data = {'id': self.parent['id'], 'root': self.parent['root'], 'cost': self.parent['cost'],
                'src_port': -1}
        for s in self.sockets:
            data['src_port'] = self.sockets.index(s)
            msg = json.dumps({'source': self.parent['id'], 'dest': 'ffff', 'type': 'bpdu', 'message': data})
            s.send(msg)
            self.bpdu_time = time() * 1000

    # update bpdu info
    def curr_bpdus(self):
        remove_rows = []
        for bpdu in self.bridge_table:
            if time() * 1000 > self.bridge_table[bpdu]['time']:
                remove_rows.append(bpdu)
        for bpdu in remove_rows:
            if bpdu == self.parent['child']:
                if self.parent['port'] != -1:
                    self.forwarding_table.clear()
                    print("Root port: " + str(id) + "/" + str(self.parent['port']))
                bridge.parent['root'] = id
                bridge.parent['child'] = id
                bridge.parent['cost'] = 0
                bridge.parent['port'] = -1

                for i in range(len(self.ignored_ports)):
                    self.ignored_ports[i] = 1

                self.broadcast_bpdu()
            del self.bridge_table[bpdu]

    # update forwarding table info
    def curr_forwarding(self):
        remove_rows = []
        for host in self.forwarding_table:
            if time() * 1000 - self.forwarding_table[host]['time'] > 500:
                remove_rows.append(host)

        for host in remove_rows:
            del self.forwarding_table[host]

    # when the bridge receives the message it transmitted
    def handle_self_loop(self, msg_id, msg_src):
        if src > msg_src:
            if self.ignored_ports[src]:
                self.forwarding_table.clear()
                print "Disabled port " + str(id) + "/" + str(src)
            self.ignored_ports[src] = 0
        elif src < msg_src:
            if self.ignored_ports[msg_src]:
                self.forwarding_table.clear()
                print "Disabled port " + str(id) + "/" + str(msg_src)
            self.ignored_ports[msg_src] = 0

    # when the bridge receives the same bridge info
    def handle_repeats(self, msg_root, msg_id, msg_cost, msg_src):
        if int(self.id, 16) > int(msg_id, 16):
            prev_port = self.bridge_table[msg_id]['src']
            if src < prev_port:
                if self.ignored_ports[prev_port]:
                    self.forwarding_table.clear()
                    print "Disabled port " + str(id) + "/" + str(prev_port)
                self.ignored_ports[prev_port] = 0
                self.change_bridge_table(msg_id, src, msg_root, msg_cost)
            else:
                self.bridge_table[msg_id]['time'] = time() * 1000 + 750
                if self.ignored_ports[src]:
                    self.forwarding_table.clear()
                    print "Disabled port " + str(id) + "/" + str(src)
                self.ignored_ports[src] = 0

    # change the bridge to a better root
    def change_root(self, msg_root, msg_id, msg_cost, msg_src):
        if not self.ignored_ports[src]:
            self.forwarding_table.clear()
            print "Designated port: " + str(id) + "/" + str(src)

        self.ignored_ports[src] = 1
        for i in range(len(self.ignored_ports)):
            self.ignored_ports[i] = 1

        if self.parent['port'] != src:
            self.forwarding_table.clear()
            print("Root port: " + str(id) + "/" + str(self.parent['port']))
        bridge.parent['root'] = msg_root
        bridge.parent['child'] = msg_id
        bridge.parent['cost'] = msg_cost + 1
        bridge.parent['port'] = src
        self.change_bridge_table(msg_id, src, msg_root, msg_cost)
        print "New root: " + str(id)
        self.broadcast_bpdu()

    # when two bridges have the same root
    def handle_same_root(self, msg_root, msg_id, msg_cost, msg_src):
        self.change_bridge_table(msg_id, src, msg_root, msg_cost)
        if msg_cost + 1 < self.parent['cost']:
            if not self.ignored_ports[src]:
                self.forwarding_table.clear()
                print "Designated port: " + str(id) + "/" + str(src)

            for i in range(len(self.ignored_ports)):
                self.ignored_ports[i] = 1
            if self.parent['port'] != src:
                self.forwarding_table.clear()
                print("Root port: " + str(id) + "/" + str(self.parent['port']))
            bridge.parent['root'] = msg_root
            bridge.parent['child'] = msg_id
            bridge.parent['cost'] = msg_cost + 1
            bridge.parent['port'] = src
            self.broadcast_bpdu()
        elif msg_cost + 1 == self.parent['cost'] and self.parent['port'] != src:
            if int(msg_id, 16) < int(self.parent['child'], 16):
                if self.ignored_ports[self.parent['port']]:
                    self.forwarding_table.clear()
                    print "Disabled port " + str(id) + "/" + str(self.parent['port'])
                self.ignored_ports[self.parent['port']] = 0
                if not self.ignored_ports[src]:
                    self.forwarding_table.clear()
                    print "Designated port: " + str(id) + "/" + str(src)
                self.ignored_ports[src] = 1
                if self.parent['port'] != src:
                    self.forwarding_table.clear()
                    print("Root port: " + str(id) + "/" + str(self.parent['port']))
                bridge.parent['root'] = msg_root
                bridge.parent['child'] = msg_id
                bridge.parent['cost'] = msg_cost + 1
                bridge.parent['port'] = src
                self.broadcast_bpdu()

            else:
                if self.ignored_ports[src]:
                    self.forwarding_table = {}
                    print "Disabled port " + str(id) + "/" + str(src)
                self.ignored_ports[src] = 0
        elif msg_cost == self.parent['cost'] and self.parent['port'] != src:
            if int(self.id, 16) > int(msg_id, 16):
                if self.ignored_ports[src]:
                    self.forwarding_table.clear()
                    print "Disabled port " + str(id) + "/" + str(src)
                self.ignored_ports[src] = 0

    # generate the spanning tree
    def generate_tree(self, message, src):
        msg_root = message['root']
        msg_id = message['id']
        msg_cost = message['cost']
        msg_src = message['src_port']

        if self.id == msg_id:
            self.handle_self_loop(msg_id, msg_src)
        elif msg_id in self.bridge_table and self.bridge_table[msg_id]['src'] != src:
            self.handle_repeats(msg_root, msg_id, msg_cost, msg_src)
        elif int(msg_root, 16) < int(self.parent['root'], 16):
            self.change_root(msg_root, msg_id, msg_cost, msg_src)
        elif int(msg_root, 16) > int(self.parent['root'], 16):
            self.change_bridge_table(msg_id, src, msg_root, msg_cost)
            if not self.ignored_ports[src]:
                self.forwarding_table.clear()
                print "Designated port: " + str(id) + "/" + str(src)
            self.ignored_ports[src] = 1
        else:
            self.handle_same_root(msg_root, msg_id, msg_cost, msg_src)

    # routing the message to other hosts and bridges
    def forwarding_message(self, msg, data, src):
        msg_src = msg['source']
        msg_dest = msg['dest']
        msg_id = msg['message']['id']

        self.forwarding_table[msg_src] = {'port': src, 'time': time() * 1000}
        if msg_dest in self.forwarding_table:
            dest_port = self.forwarding_table[msg_dest]['port']
            if (dest_port == src):
                print("Not forwarding message " + str(msg_id))
            else:
                if self.ignored_ports[dest_port] == 1:
                    print("Forwarding message " + str(msg_id) + " to port " + str(dest_port))
                    self.sockets[dest_port].send(data)
        else:
            print("Broadcasting message " + str(msg_id) + " to all ports")
            for s in self.sockets:
                port = self.sockets.index(s)
                if port != src and self.ignored_ports[port]:
                    s.send(data)


# main function
if __name__ == "__main__":
    id = sys.argv[1]
    LAN = sys.argv[2:]
    bridge = Bridge(id, LAN)
    bridge.parent['id'] = id
    bridge.parent['root'] = id
    bridge.parent['child'] = id
    bridge.parent['cost'] = 0
    bridge.parent['port'] = -1

    bridge.sock()
    print "Bridge " + id + " starting up\n"

    while 1:
        if time() * 1000 - bridge.bpdu_time >= 500:
            bridge.broadcast_bpdu()

        bridge.curr_bpdus()
        bridge.curr_forwarding()

        ready, ignore, ignore2 = select.select(bridge.sockets, [], [], 0.1)

        # Reads from each of the ready sockets
        for x in ready:
            data = x.recv(1500)
            # Convert JSON message to Python dict
            msg = json.loads(data)
            message = msg['message']
            src = bridge.sockets.index(x)
            type = msg['type']
            if type == 'bpdu':
                bridge.generate_tree(message, src)
            elif type == 'data':
                if (bridge.ignored_ports[src]):
                    bridge.forwarding_message(msg, data, src)
                else:
                    print("Not forwarding message " + str(msg['message']['id']))
