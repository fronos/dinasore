import socket
import struct


class SUBSCRIBE_1:

    def __init__(self):
        self.QO = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def schedule(self, event_name, event_value, QI, ID):
        self.QO = QI
        if event_name == 'INIT':
            return self.init(ID, event_value)

        elif event_name == 'RSP':
            return self.response()

    def init(self, ID, event_value):
        pair = ID.split(':')
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((pair[0], int(pair[1])))
        m_req = struct.pack("4sl", socket.inet_aton(pair[0]), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, m_req)

        return [event_value, None, self.QO, None, None]

    def response(self):
        data, address = self.sock.recvfrom(1024)
        data_str = data.decode(encoding='utf-8').split(':')
        event = int(data_str[0])
        value = int(data_str[1])
        return [None, event, self.QO, None, value]