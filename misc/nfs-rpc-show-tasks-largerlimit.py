#!/usr/bin/env/python
from __future__ import print_function

__author__ = "Dave Wysochanski"
__version__ = "0.1"

from pykdump.API import *
import socket
import struct

from include.linux.sunrpc.sched_h import rpc_task

MAX_RPC_TASKS = 1000000

def get_oldest_task(tasks):
    oldest_task = 0
    oldest_tk_start = LONG_MAX
    for t in tasks:
        try:
            tk_start = t.tk_start.tv64
        except:
            tk_start = t.tk_start
        if tk_start < oldest_tk_start:
            oldest_task = t
            oldest_tk_start = tk_start
    return oldest_task

# Taken from upstream nfsshow.py commit f957f9a6a7e0a218c62396072cde58f26c72ce0f
# Warning: on older kernels:
# struct net_generic {
#        unsigned int len;
#
# and on newer ones:
# struct net_generic {
#	union {
#		struct {
#			unsigned int len;
#			struct rcu_head rcu;
#		} s;

# In the latter case, net_generic() returns ng->ptr[id] instead of
# ng->ptr[id-1]

def net_generic(net, net_id):
    ng = net.gen
    ptr = ng.ptr
    try:
        ng_len = ng.len
        newstyle = False
    except KeyError:
        ng_len = ng.s.len
        newstyle = True
    #print(net_id, ng_len)
    assert (not (net_id == 0 or net_id > ng_len))
    addr = ptr[net_id] if newstyle else ptr[net_id - 1]
    return addr

# Get sunrpc_net
def get_sunrpc_net():
    if (not symbol_exists("sunrpc_net_id")):
        return 0
    net_id = readSymbol("sunrpc_net_id")
    net = readSymbol("init_net")
    return net_generic(net, net_id)

# Get all RPC clients for kernels where they exist
def get_all_rpc_clients():
    all_clients = sym2addr("all_clients")
    print("all_clients = 0x%x" % all_clients)
    if (all_clients != -1 and all_clients != 0):
        return readSUListFromHead(all_clients, "cl_clients", "struct rpc_clnt")
    ns_list = sym2addr("net_namespace_list")
    sunrpc_net = get_sunrpc_net()
    print("ns_list = 0x%x" % ns_list)
    if (ns_list != -1 and sunrpc_net != 0):
        for n in readSUListFromHead(ns_list, "list", "struct net"):
            print("(struct sunrpc_net *)0x%x" % sunrpc_net)
            rpc_net = readSU("struct sunrpc_net", sunrpc_net)
            print("(struct list_head *)0x%x" % rpc_net.all_clients)
            return readSUListFromHead(rpc_net.all_clients, "cl_clients", "struct rpc_clnt")
    return []

# FIXME: This does not work on RHEL7 yet
def get_all_rpc_tasks():
    all_taddr = sym2addr("all_tasks")
    print("all_tasks = 0x%x" % all_taddr)
    if (all_taddr != -1 and all_taddr != 0):
        return readSUListFromHead(all_taddr, "tk_task", "struct rpc_task", MAX_RPC_TASKS)

    out = []
    allc = get_all_rpc_clients()
    for cl in allc:
        out += readSUListFromHead(long(cl.cl_tasks), "tk_task",
                                   "struct rpc_task", MAX_RPC_TASKS)

    return out


def rpc_show_tasks():
    tasks = get_all_rpc_tasks()
    if len(tasks) == 0:
        print("No NFS RPC tasks found");
        return

    for t in tasks:
        task = rpc_task(t)
        task.print_verbose()

    t = rpc_task(get_oldest_task(tasks))
    print("RPC task with smallest tk_start value (oldest RPC task): ");
    t.print_verbose()

# thanks stackoverflow
def auto_int(x):
    return int(x,0)

if __name__ == '__main__':
    rpc_show_tasks()
