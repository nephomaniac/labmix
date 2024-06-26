#!/usr/bin/python
"""
Simple IP packet generator/client test tool.
Provides very limited support for testing specific IP protocols. Primarily used to test
specific network paths in a cloud or data center traversing firewalls/security groups, nat points,
etc..
"""
from os.path import abspath, basename
from random import getrandbits
import array
import socket
import struct
import sys
import time
from optparse import OptionParser, OptionValueError
# ICMP TYPES
ICMP_ECHO_REQUEST = 8
ICMP_EHCO_REPLY = 0
# SCTP TYPES
CHUNK_DATA = 0
CHUNK_INIT = 1
CHUNK_HEARTBEAT = 3
# DEBUG LEVELS
TRACE = 3
DEBUG = 2
INFO = 1
QUIET = 0
VERBOSE_LVL = INFO


def get_script_path():
    """
    Returns the path to this script
    """
    try:
        import inspect
    except ImportError:
        return None
    return abspath(inspect.stack()[0][1])


def sftp_file(sshconnection, verbose_level=DEBUG):
    """
    Uploads this script using the sshconnection's sftp interface to the sshconnection host.
    :param sshconnection: SshConnection object
    :param verbose_level: The level at which this method should log it's output.
    """
    script_path = get_script_path()
    script_name = basename(script_path)
    sshconnection.sftp_put(script_path, script_name)
    debug('Done Copying script:"{0}" to "{1}"'.format(script_name, sshconnection.host),
          verbose_level)
    return script_name


def debug(msg, level=DEBUG):
    """
    Write debug info to stdout filtering on the set verbosity level and prefixing each line
    with a '#' to allow for easy parsing of results from output.
    :param msg: string to print
    :param level: verbosity level of this message
    :return: None
    """
    if not VERBOSE_LVL:
        return
    if VERBOSE_LVL >= level:
        for line in str(msg).splitlines():
            sys.stdout.write("# {0}\n".format(str(line)))
            sys.stdout.flush()


def get_src(dest):
    """
    Attempts to learn the source IP from the outbound interface used to reach the provided
    destination
    :param dest: destination address/ip
    :return: local ip
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.connect((dest, 1))
    source_ip = s.getsockname()[0]
    s.close()
    return source_ip


def remote_sender(ssh, dst_addr, port=None, srcport=None, proto=17, count=1, socktimeout=10,
                  timeout=15, data=None, verbose=False, interval=.1, cb=None, cbargs=None):
    """
    Uses the ssh SshConnection obj's sftp interface to transfer this script to the remote
    machine and execute it with the parameters provided. Will return the combined stdout & stderr
    of the remote session.

    :param ssh: SshConnection object to run this script
    :param dst_addr: Where to send packets to
    :param port: The destination port of the packets (depending on protocol support)
    :param srcport: The source port to use in the sent packets
    :param proto: The IP protocol number (ie: 1=icmp, 6=tcp, 17=udp, 132=sctp)
    :param count: The number of packets to send
    :param timeout: The max amount of time allowed for the remote command to execute
    :param socktimeout: Time out used for socket operations
    :param data: Optional data to append to the built packet(s)
    :param verbose: Boolean to enable/disable printing of debug info
    :param cb: A method/function to be used as a call back to handle the ssh command's output
               as it is received. Must return type sshconnection.SshCbReturn
    :param cbargs: list of args to be provided to callback cb.
    :return: :raise RuntimeError: If remote command return status != 0
    """
    if verbose:
        verbose_level = VERBOSE_LVL
    else:
        verbose_level = DEBUG
    script = sftp_file(ssh, verbose_level=verbose_level)
    # destip, proto, dstport=345, ptype=None, payload=None

    cmd = "python {0} -o {1} -c {2} -d {3} -i {4} -t {5} "\
        .format(script, proto, count, dst_addr, interval, socktimeout)
    if port:
        cmd += " -p {0} ".format(port)
    if srcport is not None:
        cmd += " -s {0} ".format(srcport)
    if data is not None:
        cmd += ' -l "{0}"'.format(data.strip('"'))
    out = ""
    debug("CMD: {0}".format(cmd), verbose_level)
    cmddict = ssh.cmd(cmd, listformat=False, timeout=timeout, cb=cb, cbargs=cbargs,
                      verbose=verbose)
    out += cmddict.get('output')
    if cmddict.get('status') != 0:
        raise RuntimeError('{0}\n"{1}" cmd failed with status:{2}, on host:{3}'
                           .format(out, cmd, cmddict.get('status'), ssh.host))
    debug(out, verbose_level)
    return out


def send_ip_packet(destip, proto=4, count=1, interval=.1, payload=None, timeout=10):
    """
    Send a raw ip packet, payload can be used to append to the IP header...
    :param destip: Destination ip
    :param proto: protocol to use, default is 4
    :param payload: optional string buffer to append to IP packet
    """
    s = None
    if payload is None:
            payload = 'IP TEST PACKET'
    payload = payload or ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
        s.settimeout(timeout)
        for x in range(0, count):
            s.sendto(payload, (destip, 0))
            time.sleep(interval)
    except socket.error as SE:
        if SE.errno == 1 and 'not permitted' in SE.strerror:
            sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
        raise
    finally:
        if s:
            s.close()


def send_sctp_packet(destip, dstport=101, srcport=100, proto=132, ptype=None, payload=None,
                     sctpobj=None, count=1, interval=.1, timeout=10):
    """
    Send Basic SCTP packets

    :param destip: Destination IP to send SCTP packet to
    :param dstport: Destination port to use in the SCTP packet
    :param srcport: Source port to use in the SCTP packet
    :param proto: Protocol number to use, default is 132 for SCTP
    :param ptype: SCTP type, default is 'init' type
    :param payload: optional payload to use in packets (ie data chunk payload)
    :param sctpobj: A pre-built sctpobj to be sent
    """
    s = None
    if payload is None:
            payload = 'SCTP TEST PACKET'
    payload = payload or ""
    if ptype is None:
        ptype = CHUNK_INIT
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
        s.setsockopt(socket.SOL_IP, socket.IP_TOS, 0x02)  # set ecn bit
        s.settimeout(timeout)
        if not sctpobj:
            sctpobj = SCTP(srcport=srcport, dstport=dstport, ptype=ptype, payload=payload)
        for x in range(0, count):
            s.sendto(sctpobj.pack(), (destip, dstport))
            time.sleep(interval)
    except socket.error as SE:
        if SE.errno == 1 and 'not permitted' in SE.strerror:
            sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
        raise
    finally:
        if s:
            s.close()


def send_udp_packet(destip, srcport=None, dstport=101, proto=17, payload=None, count=1,
                    interval=.1, timeout=10):
    """
    Send basic UDP packet

    :param destip: Destination IP to send UDP packet
    :param srcport: source port to use in the UDP packet, if provided will attempt to bind
                    to this port
    :param dstport: destination port to use in the UDP packet
    :param proto: protocol number, default is 17 for UDP
    :param payload: optional payload for this packet
    """
    s = None
    if payload is None:
            payload = 'UDP TEST PACKET'
    payload = payload or ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto)
        s.settimeout(timeout)
        if srcport is not None:
            s.bind(('', srcport))
        for x in range(0, count):
            s.sendto(payload, (destip, dstport))
            time.sleep(interval)
    except socket.error as SE:
        if SE.errno == 1 and 'not permitted' in SE.strerror:
            sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
        raise
    finally:
        if s:
            s.close()


def send_tcp_packet(destip, dstport=101, srcport=None, proto=6, payload=None, bufsize=None,
                    count=1, interval=.1, timeout=10):
    """
    Send basic TCP packet

    :param destip: Destination IP to send TCP packet
    :param dstport: destination port to use in this TCP packet
    :param srcport: source port to use in this TCP packet. If provided will attempt to bind
                    to this port
    :param proto: protocol number, default is 6 for TCP
    :param payload: optional payload for this packet
    :param bufsize: Buffer size for recv() on socket after sending packet
    :return: Any data read on socket after sending the packet
    """
    data = ''
    s = None
    if payload is None:
            payload = 'TCP TEST PACKET'
    payload = payload or ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
        s.settimeout(timeout)
        if srcport is not None:
            s.bind(('', srcport))
        s.connect((destip, dstport))
        for x in range(0, count):
            s.send(payload)
            if bufsize:
                data += s.recv(bufsize)
            time.sleep(interval)
    except socket.error as SE:
        if SE.errno == 1 and 'not permitted' in SE.strerror:
            sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
        raise
    finally:
        if s:
            s.close()
    return data


def send_icmp_packet(destip, id=1234, seqnum=1, code=0, proto=1, ptype=None, count=1, interval=.1,
                     payload='ICMP TEST PACKET', timeout=10):
    """
    Send basic ICMP packet (note: does not wait for, or validate a response)

    :param destip: Destination IP to send ICMP packet to
    :param id: ID, defaults to '1234'
    :param seqnum: Sequence number, defaults to '1'
    :param code: ICMP subtype, default to 0
    :param proto: protocol number, defaults to 1 for ICMP
    :param ptype: ICMP type, defaults to icmp echo request
    :param payload: optional payload
    """
    if payload is None:
            payload = 'ICMP TEST PACKET'
    payload = payload or ""
    s = None
    if ptype is None:
        ptype = ICMP_ECHO_REQUEST
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
        s.settimeout(timeout)
        icmp = ICMP(destaddr=destip, id=id, seqnum=seqnum, code=code, ptype=ptype, payload=payload)
        for x in range(0, count):
            s.sendto(icmp.pack(), (destip, 0))
            time.sleep(interval)
    except socket.error as SE:
        if SE.errno == 1 and 'not permitted' in SE.strerror:
            sys.stderr.write('Permission error creating socket, try with sudo, root...?\n')
        raise
    finally:
        if s:
            s.close()


def send_packet(destip, proto, srcport=None, dstport=345, ptype=None, payload=None, count=1,
                interval=.1, timeout=10, verbose=DEBUG):
    """
    Wrapper to sends packets of varying types
    :param destip: Destination IP to send packet to
    :param proto: IP protocol number (ie:1=icmp, 6=tcp, 17=udp, 132=sctp)
    :param srcport: Source port to use in packet (Depends on protocol)
    :param dstport: Destination port to use in packet (Depends on protocol)
    :param ptype: Packet type (if protocol supports subtypes)
    :param payload: Optional payload to send with packet
    :param count: Number of packets to send
    :param verbose: Sets the level info will be logged at
    """

    debug('send_packet: destip:{0}, dstport:{1}, proto:{2}, ptype:{3}, count:{4}, interval:{5}'
          .format(destip, dstport, proto, ptype, count, interval), level=verbose)
    if proto in [1, 'icmp']:
        send_icmp_packet(destip=destip, ptype=ptype, payload=payload, count=count,
                         interval=interval, timeout=timeout)
    elif proto in [6, 'tcp']:
        send_tcp_packet(destip=destip, srcport=srcport, dstport=dstport, payload=payload,
                        count=count, interval=interval, timeout=timeout)
    elif proto in [17, 'udp']:
        send_udp_packet(destip=destip, srcport=srcport, dstport=dstport, payload=payload,
                        count=count, interval=interval, timeout=timeout)
    elif proto in [132, 'sctp']:
        send_sctp_packet(destip=destip, srcport=srcport, ptype=ptype, dstport=dstport,
                         payload=payload, count=count, interval=interval, timeout=timeout)
    else:
        send_ip_packet(destip=destip, proto=proto, payload=payload, count=count, interval=interval,
                       timeout=timeout)


###################################################################################################
#                                   ICMP PACKET BUILDERS
###################################################################################################

class ICMP(object):
    def __init__(self, destaddr, id=1234, seqnum=1, code=0, ptype=None,
                 payload=None):

        self.destaddr = destaddr
        if payload is None:
            payload = 'ICMP TEST PACKET'
        self.payload = payload or ""
        self.icmptype = ptype or ICMP_ECHO_REQUEST
        self.id = id
        self.code = code
        self.seqnum = seqnum

    def pack(self):
        tmp_checksum = 0
        header = struct.pack("bbHHh", self.icmptype, self.code, tmp_checksum, self.id, self.seqnum)
        fin_checksum = checksum(header + self.payload)
        header = struct.pack("bbHHh", self.icmptype, self.code, socket.htons(fin_checksum),
                             self.id, self.seqnum)
        packet = header + self.payload
        return packet


###################################################################################################
#                                   SCTP PACKET BUILDERS
###################################################################################################

class InitChunk(object):
    def __init__(self, tag=None, a_rwnd=62464, outstreams=10, instreams=65535, tsn=None,
                 param_data=None):
        self.tag = tag or getrandbits(32) or 3
        self.a_rwnd = a_rwnd
        self.outstreams = outstreams or 1  # 0 is invalid
        self.instreams = instreams or 1  # 0 is invalid
        self.tsn = tsn or getrandbits(32) or 4
        if param_data is None:
            param_data = ""
            suppaddrtypes = SctpSupportedAddrTypesParam()
            param_data += suppaddrtypes.pack()
            ecn = SctpEcnParam()
            param_data += ecn.pack()
            fwdtsn = SctpFwdTsnSupportParam()
            param_data += fwdtsn.pack()
        self.param_data = param_data

    def pack(self):
        packet = struct.pack('!IIHHI', self.tag, self.a_rwnd, self.outstreams, self.instreams,
                             self.tsn)
        if self.param_data:
            packet += self.param_data
        return packet


class SctpIPv4Param(object):
    def __init__(self, type=5, length=8, ipv4addr=None):
        self.type = type
        self.length = length
        self.addr = ipv4addr

    def pack(self):
        packet = struct.pack('!HHI', self.type, self.length, self.addr)
        return packet


class SctpSupportedAddrTypesParam(object):
    def __init__(self, ptype=12, addr_types=None):
        ipv4 = 5
        # ipv6 = 6
        # hostname = 11
        if addr_types is None:
            addr_types = [ipv4]
        if not isinstance(addr_types, list):
            addr_types = [addr_types]
        self.addr_types = addr_types
        self.ptype = 12
        self.length = 4 + (2 * len(self.addr_types))

    def pack(self):
        fmt = '!HH'
        contents = [self.ptype, self.length]
        for atype in self.addr_types:
            fmt += 'H'
            contents.append(atype)
        contents = tuple(contents)
        packet = struct.pack(fmt, *contents)
        # add padding
        if len(self.addr_types) % 2:
            packet += struct.pack("H", 0)
        return packet


class SctpEcnParam(object):
    def __init__(self, ptype=32768):
        self.ptype = ptype
        self.length = 4

    def pack(self):
        return struct.pack('!HH', self.ptype, self.length)


class SctpFwdTsnSupportParam(object):
    def __init__(self, ptype=49152):
        self.ptype = ptype
        self.length = 4

    def pack(self):
        return struct.pack('!HH', self.ptype, self.length)


class DataChunk(object):
    def __init__(self, tsn=1, stream_id=12345, stream_seq=54321, payload_proto=0, payload=None):
        if payload is None:
            payload = "TEST SCTP DATA CHUNK"
        self.payload = payload
        self.tsn = tsn
        self.stream_id = stream_id
        self.stream_seq = stream_seq
        self.payload_proto = payload_proto

    @property
    def length(self):
        return 12 + len(self.payload)

    def pack(self):
        packet = struct.pack('!iHHi', self.tsn, self.stream_id, self.stream_seq,
                             self.payload_proto)
        packet += self.payload
        return packet


class HeartBeatChunk(object):
    def __init__(self, parameter=1, payload=None):
        self.parameter = parameter
        if payload is None:
            payload = str(getrandbits(64))
        self.hb_info = payload
        self.hb_info_length = 4 + len(payload)

    def pack(self):
        chunk = struct.pack('!HH', self.parameter, self.hb_info_length)
        chunk += self.hb_info
        return chunk


class ChunkHdr(object):
    def __init__(self, chunktype=None, flags=0, payload=None, chunk=None):
        if chunktype is None:
            chunktype = 1
        self.chunktype = chunktype
        self.chunkflags = flags
        if chunk:
            self.chunkobj = chunk
        elif chunktype == 0:
            self.chunkobj = DataChunk(payload=payload)
        elif chunktype == 1:
            self.chunkobj = InitChunk()
        elif chunktype == 4:
            self.chunkobj = HeartBeatChunk(payload=payload)
        self.chunk_data = self.chunkobj.pack()
        self.chunklength = 4
        # SCTP header plus rest of packet = length?
        self.chunklength = 4 + len(self.chunk_data)

    def pack(self):
        chunk = struct.pack('!bbH', self.chunktype, self.chunkflags, self.chunklength)
        packet = chunk + self.chunk_data
        return packet


class SCTP(object):
    """
    Chunk Types
    0	DATA	Payload data
    1	INIT	Initiation
    2	INIT ACK	initiation acknowledgement
    3	SACK	Selective acknowledgement
    4	HEARTBEAT	Heartbeat request
    5	HEARTBEAT ACK	Heartbeat acknowledgement
    6	ABORT	Abort
    7	SHUTDOWN	Shutdown
    8	SHUTDOWN ACK	Shutdown acknowledgement
    9	ERROR	Operation error
    10	COOKIE ECHO	State cookie
    11	COOKIE ACK	Cookie acknowledgement
    12	ECNE	Explicit congestion notification echo (reserved)
    13	CWR	Congestion window reduced (reserved)
    14	SHUTDOWN COMPLETE

    Chunk Flags
    # I - SACK chunk should be sent back without delay.
    # U - If set, this indicates this data is an unordered chunk and the stream sequence number
          is invalid. If an unordered chunk is fragmented then each fragment has this flag set.
    # B - If set, this marks the beginning fragment. An unfragmented chunk has this flag set.
    # E - If set, this marks the end fragment. An unfragmented chunk has this flag set
    """
    def __init__(self, srcport, dstport, tag=None, ptype=None, payload=None, chunk=None):
        self.src = srcport
        self.dst = dstport
        self.checksum = 0
        if ptype is None:
            ptype = CHUNK_INIT
            tag = 0  # Verification tag is set to 0 for init
        if tag is None:
            if ptype == CHUNK_INIT:
                tag = 0
            else:
                tag = getrandbits(16)
        self.tag = tag
        chunk = chunk or ChunkHdr(chunktype=ptype, payload=payload)
        self.chunk = chunk.pack()

    def pack(self, src=None, dst=None, tag=None, do_checksum=True):
        src = src or self.src
        dst = dst or self.dst
        verification_tag = tag or self.tag
        packet = struct.pack('!HHII', src, dst, verification_tag, 0)
        chunk = self.chunk
        if not do_checksum:
            packet += chunk
            return packet
        pktchecksum = cksum(packet + chunk)
        # Rebuild the packet with the checksum
        packet = struct.pack('!HHII', src, dst,
                             verification_tag, pktchecksum)
        packet += chunk
        return packet


###################################################################################################
#  Borrowed checksum method, big thanks to the following...
#  (Including this in this file for ease of transfer when testing this on remote VMs as a
#  alone script.)
###################################################################################################

def checksum(source_string):
    """
    From: https://github.com/samuel/python-ping
    Copyright (c) Matthew Dixon Cowles, <http://www.visi.com/~mdc/>.
    Distributable under the terms of the GNU General Public License
    version 2. Provided with no warranties of any sort.
    """
    # I'm not too confident that this is right but testing seems to
    # suggest that it gives the same answers as in_cksum in ping.c.
    sum = 0
    count_to = (len(source_string) / 2) * 2
    count = 0
    while count < count_to:
        this_val = ord(source_string[count + 1])*256+ord(source_string[count])
        sum = sum + this_val
        sum = sum & 0xffffffff  # Necessary?
        count = count + 2
    if count_to < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])
        sum = sum & 0xffffffff  # Necessary?
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


###################################################################################################
#  Borrowed crc32c for python, big thanks to the following...
#  (Including this in this file for ease of transfer when testing this on remote VMs as a
#  alone script.)
###################################################################################################
#  """
#  Copyright (c) 2004 Dug Song <dugsong@monkey.org>
#   All rights reserved, all wrongs reversed.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions
#   are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#   3. The names of the authors and copyright holders may not be used to
#      endorse or promote products derived from this software without
#      specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
#   INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
#   AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
#   THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  """
# CRC-32C Checksum
# http://tools.ietf.org/html/rfc3309

crc32c_table = (
    0x00000000, 0xF26B8303, 0xE13B70F7, 0x1350F3F4, 0xC79A971F,
    0x35F1141C, 0x26A1E7E8, 0xD4CA64EB, 0x8AD958CF, 0x78B2DBCC,
    0x6BE22838, 0x9989AB3B, 0x4D43CFD0, 0xBF284CD3, 0xAC78BF27,
    0x5E133C24, 0x105EC76F, 0xE235446C, 0xF165B798, 0x030E349B,
    0xD7C45070, 0x25AFD373, 0x36FF2087, 0xC494A384, 0x9A879FA0,
    0x68EC1CA3, 0x7BBCEF57, 0x89D76C54, 0x5D1D08BF, 0xAF768BBC,
    0xBC267848, 0x4E4DFB4B, 0x20BD8EDE, 0xD2D60DDD, 0xC186FE29,
    0x33ED7D2A, 0xE72719C1, 0x154C9AC2, 0x061C6936, 0xF477EA35,
    0xAA64D611, 0x580F5512, 0x4B5FA6E6, 0xB93425E5, 0x6DFE410E,
    0x9F95C20D, 0x8CC531F9, 0x7EAEB2FA, 0x30E349B1, 0xC288CAB2,
    0xD1D83946, 0x23B3BA45, 0xF779DEAE, 0x05125DAD, 0x1642AE59,
    0xE4292D5A, 0xBA3A117E, 0x4851927D, 0x5B016189, 0xA96AE28A,
    0x7DA08661, 0x8FCB0562, 0x9C9BF696, 0x6EF07595, 0x417B1DBC,
    0xB3109EBF, 0xA0406D4B, 0x522BEE48, 0x86E18AA3, 0x748A09A0,
    0x67DAFA54, 0x95B17957, 0xCBA24573, 0x39C9C670, 0x2A993584,
    0xD8F2B687, 0x0C38D26C, 0xFE53516F, 0xED03A29B, 0x1F682198,
    0x5125DAD3, 0xA34E59D0, 0xB01EAA24, 0x42752927, 0x96BF4DCC,
    0x64D4CECF, 0x77843D3B, 0x85EFBE38, 0xDBFC821C, 0x2997011F,
    0x3AC7F2EB, 0xC8AC71E8, 0x1C661503, 0xEE0D9600, 0xFD5D65F4,
    0x0F36E6F7, 0x61C69362, 0x93AD1061, 0x80FDE395, 0x72966096,
    0xA65C047D, 0x5437877E, 0x4767748A, 0xB50CF789, 0xEB1FCBAD,
    0x197448AE, 0x0A24BB5A, 0xF84F3859, 0x2C855CB2, 0xDEEEDFB1,
    0xCDBE2C45, 0x3FD5AF46, 0x7198540D, 0x83F3D70E, 0x90A324FA,
    0x62C8A7F9, 0xB602C312, 0x44694011, 0x5739B3E5, 0xA55230E6,
    0xFB410CC2, 0x092A8FC1, 0x1A7A7C35, 0xE811FF36, 0x3CDB9BDD,
    0xCEB018DE, 0xDDE0EB2A, 0x2F8B6829, 0x82F63B78, 0x709DB87B,
    0x63CD4B8F, 0x91A6C88C, 0x456CAC67, 0xB7072F64, 0xA457DC90,
    0x563C5F93, 0x082F63B7, 0xFA44E0B4, 0xE9141340, 0x1B7F9043,
    0xCFB5F4A8, 0x3DDE77AB, 0x2E8E845F, 0xDCE5075C, 0x92A8FC17,
    0x60C37F14, 0x73938CE0, 0x81F80FE3, 0x55326B08, 0xA759E80B,
    0xB4091BFF, 0x466298FC, 0x1871A4D8, 0xEA1A27DB, 0xF94AD42F,
    0x0B21572C, 0xDFEB33C7, 0x2D80B0C4, 0x3ED04330, 0xCCBBC033,
    0xA24BB5A6, 0x502036A5, 0x4370C551, 0xB11B4652, 0x65D122B9,
    0x97BAA1BA, 0x84EA524E, 0x7681D14D, 0x2892ED69, 0xDAF96E6A,
    0xC9A99D9E, 0x3BC21E9D, 0xEF087A76, 0x1D63F975, 0x0E330A81,
    0xFC588982, 0xB21572C9, 0x407EF1CA, 0x532E023E, 0xA145813D,
    0x758FE5D6, 0x87E466D5, 0x94B49521, 0x66DF1622, 0x38CC2A06,
    0xCAA7A905, 0xD9F75AF1, 0x2B9CD9F2, 0xFF56BD19, 0x0D3D3E1A,
    0x1E6DCDEE, 0xEC064EED, 0xC38D26C4, 0x31E6A5C7, 0x22B65633,
    0xD0DDD530, 0x0417B1DB, 0xF67C32D8, 0xE52CC12C, 0x1747422F,
    0x49547E0B, 0xBB3FFD08, 0xA86F0EFC, 0x5A048DFF, 0x8ECEE914,
    0x7CA56A17, 0x6FF599E3, 0x9D9E1AE0, 0xD3D3E1AB, 0x21B862A8,
    0x32E8915C, 0xC083125F, 0x144976B4, 0xE622F5B7, 0xF5720643,
    0x07198540, 0x590AB964, 0xAB613A67, 0xB831C993, 0x4A5A4A90,
    0x9E902E7B, 0x6CFBAD78, 0x7FAB5E8C, 0x8DC0DD8F, 0xE330A81A,
    0x115B2B19, 0x020BD8ED, 0xF0605BEE, 0x24AA3F05, 0xD6C1BC06,
    0xC5914FF2, 0x37FACCF1, 0x69E9F0D5, 0x9B8273D6, 0x88D28022,
    0x7AB90321, 0xAE7367CA, 0x5C18E4C9, 0x4F48173D, 0xBD23943E,
    0xF36E6F75, 0x0105EC76, 0x12551F82, 0xE03E9C81, 0x34F4F86A,
    0xC69F7B69, 0xD5CF889D, 0x27A40B9E, 0x79B737BA, 0x8BDCB4B9,
    0x988C474D, 0x6AE7C44E, 0xBE2DA0A5, 0x4C4623A6, 0x5F16D052,
    0xAD7D5351
    )


def add(crc, buf):
    buf = array.array('B', buf)
    for b in buf:
        crc = (crc >> 8) ^ crc32c_table[(crc ^ b) & 0xff]
    return crc


def done(crc):
    tmp = ~crc & 0xffffffff
    b0 = tmp & 0xff
    b1 = (tmp >> 8) & 0xff
    b2 = (tmp >> 16) & 0xff
    b3 = (tmp >> 24) & 0xff
    crc = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3
    return crc


def cksum(buf):
    """Return computed CRC-32c checksum."""
    return done(add(0xffffffff, buf))
###################################################################################################
# end of borrowed crc32c for python
###################################################################################################


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-p", "--dstport", dest="dstport", type="int", default=101,
                      help="Destination Port", metavar="PORT")
    parser.add_option("-s", "--srcport", dest="srcport", type="int", default=100,
                      help="Source Port", metavar="PORT")
    parser.add_option("-c", "--count", dest="count", type="int", default=1,
                      help="Number of packets to send", metavar="COUNT")
    parser.add_option("-i", "--interval", dest="interval", type="float", default=.1,
                      help="Time interval between sending packets, default='.1'",
                      metavar="INTERVAL")
    parser.add_option("-d", "--dst", dest="destip", default=None,
                      help="Destination ip", metavar="IP")
    parser.add_option("-o", "--proto", dest="proto", type="int", default=17,
                      help="Protocol number(Examples: 1:icmp, 6:tcp, 17:udp, 132:sctp), "
                           "default:17", metavar="PROTOCOL")
    parser.add_option("-l", "--payload", dest="payload", default=None,
                      help="Chunk, data, payload, etc", metavar="DATA")
    parser.add_option("-v", "--verbose", dest="verbose", type='int', default=DEBUG,
                      help="Verbose level, 0=quiet, 1=info, 2=debug, 3=trace. Default=1")
    parser.add_option("-t", "--socktimeout", dest='socktimeout', type='float', default=10,
                      help='Socket timeout in seconds', metavar='TIMEOUT')

    options, args = parser.parse_args()
    if not options.destip:
        raise OptionValueError("'-d / --dst' for destination IP/Addr must be provided")
    VERBOSE_LVL = options.verbose
    destip = options.destip
    proto = options.proto
    srcport = options.srcport
    interval = options.interval
    socktimeout = options.socktimeout
    if srcport is not None:
        srcport = int(srcport)
    dstport = int(options.dstport)
    payload = options.payload
    count = options.count
    send_packet(destip=destip, proto=proto, srcport=srcport, dstport=dstport, payload=payload,
                count=count, interval=interval, timeout=socktimeout)
