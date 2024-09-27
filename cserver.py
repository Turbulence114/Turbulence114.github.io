import hivemind
from typing import Optional, List
from hivemind.p2p import PeerID
from multiaddr import Multiaddr
import threading
import time
import hivemind.utils
import petals.cli.run_server
from multiprocessing import Process, Pipe, connection
import sys

logger = hivemind.utils.get_logger(__name__)
# get_dht_time = 

class CServer:
    group_info: dict
    initial_peers: list

    def __init__(
        self,
        initial_peers: Optional[List[str]],
        flop: float,
        memory: float,
        zone_key: str
    ):
        self.zone_key = zone_key
        send, recv = Pipe()
        self.dht = hivemind.DHT(start=True, initial_peers=initial_peers, send_channel = send)
        peer_id = Multiaddr(self.dht.get_visible_maddrs()[0])
        self.initial_peers = initial_peers
        self.update_cserver_handler = threading.Thread(target = self.update_cserver_info,args=(flop, memory, zone_key, peer_id), daemon= True)
        self.update_cserver_handler.start()
        self.process_msg_handler = Process(target=self.process_msg, args=(recv, self.dht))
        self.process_msg_handler.start()
    
    def update_cserver_info(self, flop: float, memory: float, zone_key:str, peer_id:Multiaddr):
        while True:
            try:
                peer_id = peer_id.__str__()
                self.dht.store(key=zone_key, subkey=peer_id, value=(flop, memory, peer_id), expiration_time=hivemind.utils.get_dht_time()+30)
            except Exception:
                print("Caught exception when store cserver info")
            time.sleep(10)

    def start_server(self):
        petals.cli.run_server.main()
    
    def process_msg(self, recv: connection.Connection, dht: hivemind.DHT):
        handles = list()
        print("cserver start process msg that from mserver")
        while(True):
            if not recv.poll():
                continue
            try:
                cmd, block = recv.recv()
                print("recv cmd:", cmd, "block: ", block)
            except:
                print("meet exception")
                for h in handles:
                    h.terminate()
                    h.join()
                sys.exit()
            if cmd=="start":
               print("start")
            elif cmd=="stop":
                
                print("we will stop a span")
            elif cmd=="transfer":
                print("we will transfer a expert")
            else:
                print("break recv msg")
                break
        for h in handles:
            h.terminate()
            h.join()
        sys.exit()